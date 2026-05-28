#!/usr/bin/env python3
import re
import json
import argparse
from pathlib import Path

SECTION_ORDER = ["intro", "verse", "chorus", "bridge", "outro"]
SECTION_SET = set(SECTION_ORDER)

# Section headers: "Verse:", "chorus", "[intro:]" etc.
SECTION_HEADER_RE = re.compile(
    r"^\s*\[?\s*(intro|verse|chorus|bridge|outro)\s*\]?\s*:?\s*$",
    re.IGNORECASE
)

# Capo lines: "capo: 0" or "[capo: 3]"
CAPO_RE = re.compile(r"^\s*\[?\s*capo\s*:\s*([+-]?\d+)\s*\]?\s*$", re.IGNORECASE)

# Field headers: "title:", "artist:"
FIELD_RE = re.compile(r"^\s*(title|artist)\s*:\s*$", re.IGNORECASE)

# A fairly generous chord token:
# Examples: C, C7, Cm, Dm7, F#maj7, Bb, Gsus4, Am7b5, C/E
CHORD_TOKEN_RE = re.compile(
    r"""
    ^
    [A-G]            # root
    (?:[#b])?        # accidental
    (?:
        maj|min|m|dim|aug|sus|add
    )?               # quality (optional)
    (?:\d+)?          # extension number (optional)
    (?:[#b]\d+)?      # alteration like b5, #9 (optional)
    (?:/[A-G](?:[#b])?)?  # slash bass (optional)
    $
    """,
    re.VERBOSE
)

# Allowed separators within chord lines
# e.g. bars, dots, hyphens used as timing markers
SEPARATOR_CHARS_RE = re.compile(r"^[\s|.\-_/]+$")


def normalise_newlines(s: str) -> str:
    return s.replace("\r\n", "\n").replace("\r", "\n")


def strip_outer_blank_lines(lines):
    i, j = 0, len(lines)
    while i < j and lines[i].strip() == "":
        i += 1
    while j > i and lines[j - 1].strip() == "":
        j -= 1
    return lines[i:j]


def is_chord_line(line: str) -> bool:
    """
    Mutually-exclusive rule:
    A chord line must consist ONLY of chord tokens plus separators/spaces.
    If any non-chord token appears, the whole line is treated as lyrics and dropped.
    """
    s = line.strip()
    if not s:
        return False

    # If it's purely separators like ". . ." or "----", drop it (timing-only)
    if SEPARATOR_CHARS_RE.match(s):
        return False

    # Split into tokens by whitespace, after normalising common separators to spaces
    cleaned = s.replace("|", " ").replace("\t", " ")
    tokens = [t.strip(",;:()[]{}") for t in cleaned.split() if t.strip(",;:()[]{}")]

    if not tokens:
        return False

    # Every token must be either a chord token or a pure separator token
    for t in tokens:
        if CHORD_TOKEN_RE.match(t):
            continue
        # Allow tokens that are just separators (rare, but safe)
        if SEPARATOR_CHARS_RE.match(t):
            continue
        return False

    return True


def extract_chord_lines(block_lines):
    kept = [ln.rstrip() for ln in block_lines if is_chord_line(ln)]
    return strip_outer_blank_lines(kept)


def parse_song(text: str):
    text = normalise_newlines(text)
    lines = text.split("\n")

    result = {
        "title": None,
        "artist": None,
        "capo": None,
        "sections": {k: None for k in SECTION_ORDER},
    }

    captured = set()

    def read_field_value(start_idx):
        vals = []
        k = start_idx
        # skip blank lines
        while k < len(lines) and lines[k].strip() == "":
            k += 1
        # take non-blank lines until blank
        while k < len(lines) and lines[k].strip() != "":
            vals.append(lines[k].rstrip())
            k += 1
        return ("\n".join(vals) if vals else None), k

    i = 0
    while i < len(lines):
        line = lines[i]

        m = CAPO_RE.match(line)
        if m and result["capo"] is None:
            result["capo"] = int(m.group(1))
            i += 1
            continue

        m = FIELD_RE.match(line)
        if m:
            field = m.group(1).lower()
            value, next_i = read_field_value(i + 1)
            if field == "title" and result["title"] is None:
                result["title"] = value
            elif field == "artist" and result["artist"] is None:
                result["artist"] = value
            i = next_i
            continue

        m = SECTION_HEADER_RE.match(line)
        if m:
            section = m.group(1).lower()
            i += 1

            buf = []
            while i < len(lines) and not SECTION_HEADER_RE.match(lines[i]):
                # don't swallow later title/artist/capo blocks
                if FIELD_RE.match(lines[i]) or CAPO_RE.match(lines[i]):
                    break
                buf.append(lines[i])
                i += 1

            if section in SECTION_SET and section not in captured:
                chord_lines = extract_chord_lines(buf)
                result["sections"][section] = "\n".join(chord_lines) if chord_lines else ""
                captured.add(section)

            continue

        i += 1

    return result


def format_pretty(result: dict) -> str:
    out = []
    title = result.get("title") or "(untitled)"
    artist = result.get("artist")
    capo = result.get("capo")

    out.append(f"TITLE: {title}")
    if artist:
        out.append(f"ARTIST: {artist}")
    if capo is not None:
        out.append(f"CAPO: {capo}")
    out.append("")

    for sec in SECTION_ORDER:
        content = result["sections"].get(sec)
        if content is None:
            continue
        out.append(sec.upper() + " (CHORDS ONLY):")
        out.append(content if content.strip() else "(no chord lines detected)")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(
        description="Extract capo/title/artist and first intro/verse/chorus/bridge/outro; chords-only with exclusive-line rule."
    )
    ap.add_argument("path", nargs="?", help="Input .txt path (defaults to stdin)")
    ap.add_argument("--json", action="store_true", help="Output JSON instead of pretty text")
    args = ap.parse_args()

    if args.path:
        text = Path(args.path).read_text(encoding="utf-8", errors="replace")
    else:
        import sys
        text = sys.stdin.read()

    parsed = parse_song(text)

    if args.json:
        print(json.dumps(parsed, indent=2, ensure_ascii=False))
    else:
        print(format_pretty(parsed), end="")


if __name__ == "__main__":
    main()


