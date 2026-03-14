import re

# Given a chord line (a line that naively contains only chords),
# for each chord in that line, alter the chord pitch by the
#  value of tone_offset.
# For example: if the current chord is Dm7, and tone_offset is (+)2
# , then the resulting chord is Em7. If the current chord is (still)
# Dm7, and the tone_offset is -2, then the resulting chord is Cm7.
# Taking a whole source chord line as an example, given:
# chord-line = "    Dm7     C      Emaj7" and tone_offset = "-1"
# the chord_line to return to the caller is
# chord-line = "    C#m7     B      D#maj7"
def alter_chord(chord_line, tone_offset)

def is_chord_line(line: str) -> bool:
    """
    Naive heuristic for detecting a chord line.

    Rules:
    1) Visible length (non‑whitespace characters only) is between 5 and 15.
    2) The line is not just whitespace.
    3) No token (split on spaces or tabs) is longer than 5 characters.
    """
    if line is None:
        return False

    # Remove trailing newline(s)
    core = line.rstrip("\r\n")

    # Rule 2: not all whitespace
    if core.strip() == "":
        return False

    # ---- FIXED RULE ----
    # visible_len excludes whitespace entirely
    visible_len = len("".join(core.split()))
    if not (5 <= visible_len <= 15):
        return False

    # Tokens: split on one or more spaces or tabs
    tokens = re.split(r"[ \t]+", core.strip())
    tokens = [t for t in tokens if t]

    # Rule 3: no token longer than 5 chars
    return all(len(tok) <= 5 for tok in tokens)

def get_song_lines(file):
    with open(file, "r") as f:
        return f.readlines()

def main(file):
    out_file = 'test_data/outfile.txt'
    lines = get_song_lines(file)
    with open(out_file, 'w') as of:
        for line in lines:
            print(line)
            if (is_chord_line(line)):

                of.write(f"That was a chord\n")
                continue
            of.write(line)


if __name__ == "__main__":
    song_file = "test_data/AHardDaysNight.txt"
    main(song_file)
