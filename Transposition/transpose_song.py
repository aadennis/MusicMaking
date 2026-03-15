#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from typing import Dict, Tuple

# .\test_data\MaggieMayShort.txt -l .\transpose_lookup_hybrid.csv -k -2

# -----------------------------
# 1) Static lookup loader (CSV)
# -----------------------------
# Expected CSV columns: source,offset,target
# Example row: D,-2,C
Lookup = Dict[Tuple[str, int], str]


def load_lookup_csv(path: str | Path) -> Lookup:
    table: Lookup = {}
    with open(path, "r", newline="", encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            src = row["source"].strip()
            off = int(row["offset"])
            tgt = row["target"].strip()
            table[(src, off)] = tgt
    # quick sanity check (12 roots × 7 offsets = 84 entries) — optional
    if len(table) < 84:
        raise ValueError(
            f"Lookup table seems incomplete: {len(table)} entries found in {path}"
        )
    return table


# --------------------------------------
# 2) Note normalization to sharp roots
# --------------------------------------
# We normalize input accidentals to your canonical sharp spellings,
# so the static CSV only needs the 12 sharp roots (C, C#, ..., B).
_ENHARMONIC_TO_SHARP = {
    "C": "C",
    "B#": "C",
    "C#": "C#",
    "DB": "C#",
    "D♭": "C#",
    "C♯": "C#",
    "D": "D",
    "D#": "D#",
    "EB": "D#",
    "E♭": "D#",
    "D♯": "D#",
    "E": "E",
    "FB": "E",
    "F♭": "E",
    "F": "F",
    "E#": "F",
    "E♯": "F",
    "F#": "F#",
    "GB": "F#",
    "G♭": "F#",
    "F♯": "F#",
    "G": "G",
    "G#": "G#",
    "AB": "G#",
    "A♭": "G#",
    "G♯": "G#",
    "A": "A",
    "A#": "A#",
    "BB": "A#",
    "B♭": "A#",
    "A♯": "A#",
    "B": "B",
    "CB": "B",
    "C♭": "B",
}


def _norm(letter: str, acc: str) -> str:
    token = (letter.upper() + acc.replace("♯", "#").replace("♭", "b")).upper()
    # convert trailing 'b' to uppercase 'B' for our dict keys (Db -> DB)
    if token.endswith("b"):
        token = token[:-1] + "B"
    return _ENHARMONIC_TO_SHARP.get(token, token)


# --------------------------------------
# 3) Chord tokenization and transposition
# --------------------------------------
# Token: root + accidental, optional quality until whitespace or '/',
# optional slash-bass of the same form.
_CHORD = re.compile(
    r"""
    (?P<root>[A-Ga-g])(?P<acc>[#b♯♭]?)   # chord root + accidental
    (?P<qual>[^/\s]*)                    # suffix/quality (m7, maj7, sus4, etc.)
    (?:/
        (?P<bass>[A-Ga-g])(?P<bacc>[#b♯♭]?)  # optional slash-bass
    )?
    """,
    re.VERBOSE,
)


def alter_chord_line(chord_line: str, k: int, lookup: Lookup) -> str:
    """
    Transpose every chord token in a chord-only line by k semitones using a static lookup.
    Whitespace/layout is preserved; qualities are left as-is; output uses sharp spelling.
    """
    if not (-3 <= k <= 3):
        raise ValueError("tone_offset must be within –3..+3 for the static lookup")

    def _xpose(letter: str, acc: str) -> str:
        src = _norm(letter, acc or "")
        try:
            return lookup[(src, k)]
        except KeyError as e:
            raise KeyError(f"Missing mapping for ({src}, {k}) in the lookup") from e

    def _repl(m: re.Match) -> str:
        root_out = _xpose(m.group("root"), m.group("acc") or "")
        qual = m.group("qual") or ""
        if m.group("bass"):
            bass_out = _xpose(m.group("bass"), m.group("bacc") or "")
            return f"{root_out}{qual}/{bass_out}"
        return f"{root_out}{qual}"

    return _CHORD.sub(_repl, chord_line)


# --------------------------------------
# 4) Whitelist-based chord-line heuristic
# --------------------------------------


def load_whitelist(path: str | Path = "whitelist_tokens.txt") -> set[str]:
    """
    Load allowed chord-quality tokens (e.g., m, sus, maj, dim).
    Tokens are treated as prefixes: a suffix starting with any of them is valid.
    Blank lines and comments (# ...) are ignored.
    """
    tokens = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            t = line.strip()
            if not t or t.startswith("#"):
                continue
            tokens.add(t)
    return tokens


def is_valid_chord_token(token: str, whitelist: set[str]) -> bool:
    """
    Determine whether a token is a chord, given the whitelist of valid quality prefixes.
    """
    m = _CHORD.fullmatch(token)
    if not m:
        return False

    qual = m.group("qual") or ""

    # Pure chord roots (A, C#, Bb) → always valid
    if qual == "":
        return True

    # Whitelist applies as "qual starts with token"
    return any(qual.startswith(w) for w in whitelist)


def load_allowed_nonchords(path="allowed_nonchord_tokens.txt"):
    tokens = set()
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            t = line.strip()
            if t and not t.startswith("#"):
                tokens.add(t)
    return tokens


def is_chord_line(line: str, whitelist: set[str], allowed_nonchords: set[str]) -> bool:
    """
    A line is a chord line if every token is either:
    - a valid chord token (uses whitelist for qualities), OR
    - an allowed non-chord token (e.g. x2, x3)
    """
    if not line or line.startswith("[") or line.strip() == "":
        return False

    tokens = line.strip().split()
    if not tokens:
        return False

    found_any_chord = False

    for tok in tokens:
        if is_valid_chord_token(tok, whitelist):
            found_any_chord = True
            continue

        if tok in allowed_nonchords:
            continue

        # Neither a chord nor an allowed extra token → it's a lyric
        return False

    return found_any_chord


# --------------------------------------
# 5) File processing
# --------------------------------------
def transpose_song_file(
    in_path: str | Path,
    out_path: str | Path,
    lookup_csv: str | Path,
    semitone_offset: int = -2,
    whitelist_path: str | Path = "whitelist_tokens.txt",
    allowed_nonchords_path: str | Path = "allowed_nonchord_tokens.txt",
) -> None:

    lookup = load_lookup_csv(lookup_csv)
    whitelist = load_whitelist(whitelist_path)
    allowed_nonchords = load_allowed_nonchords(allowed_nonchords_path)

    in_path = Path(in_path)
    out_path = Path(out_path)

    with in_path.open("r", encoding="utf-8") as fin, out_path.open(
        "w", encoding="utf-8", newline=""
    ) as fout:
        for line in fin:
            if is_chord_line(line, whitelist, allowed_nonchords):
                fout.write(alter_chord_line(line, semitone_offset, lookup))
            else:
                fout.write(line)


# --------------------------------------
# 6) CLI
# --------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Transpose chord lines in a song file using a static CSV lookup."
    )
    p.add_argument(
        "input",
        nargs="?",
        default="AHardDaysNight.txt",
        help="Path to the source song text file",
    )
    p.add_argument(
        "-o",
        "--output",
        default=None,
        help="Path to the output file (default: <input>_transposed_<k>.txt)",
    )
    p.add_argument(
        "-l",
        "--lookup",
        default="transpose_lookup_hybrid.csv",
        help="Path to the static CSV lookup",
    )
    p.add_argument(
        "-k",
        "--semitones",
        type=int,
        default=-2,
        help="Semitone offset (–3..+3); default: -2",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    p = build_parser()
    args = p.parse_args(argv)

    in_path = Path(args.input)
    if not args.output:
        stem = in_path.stem
        out_path = in_path.with_name(f"{stem}_transposed_{args.semitones}.txt")
    else:
        out_path = Path(args.output)

    transpose_song_file(
        in_path=in_path,
        out_path=out_path,
        lookup_csv=args.lookup,
        semitone_offset=args.semitones,
        whitelist_path="whitelist_tokens.txt",
        allowed_nonchords_path="allowed_nonchord_tokens.txt",
    )
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
