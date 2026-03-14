import re

def is_chord_line(line: str) -> bool:
    """
    Naive heuristic for detecting a chord line.

    Rules (as specified):
    1) The line contains between 5 and 15 characters (inclusive).
       We count visible characters after stripping trailing newlines,
       but we keep internal spaces/tabs as part of the length.
    2) The line consists of more than just whitespace.
    3) When splitting on spaces/tabs, no single token exceeds 5 characters.

    This is intentionally naive and will generate false positives/negatives
    on real-world data (e.g., lots of spacing, annotations, etc.).
    """
    if line is None:
        return False

    # Remove trailing newline(s) but keep internal whitespace as-is
    core = line.rstrip("\r\n")

    # Rule 2: not just whitespace
    if core.strip() == "":
        return False

    # Rule 1: visible length in [5, 15]
    visible_len = len(core)
    if not (5 <= visible_len <= 15):
        return False

    # Rule 3: split on SPACE or TAB specifically (not all whitespace),
    # and ensure max token length <= 5
    tokens = re.split(r"[ \t]+", core.strip())

    # Empty tokens can occur if there were leading/trailing separators after strip? (No.)
    # Still, guard defensively:
    tokens = [t for t in tokens if t]

    # Enforce the per-token length rule
    return all(len(tok) <= 5 for tok in tokens)
     
def get_song_lines(file):
    with open(file, 'r') as f:
            return f.readlines()
         
def main(file):
    lines = get_song_lines(file)
    for line in lines:
            print(line)
            print(is_chord_line(line))

if __name__ == "__main__":
  song_file = 'test_data/AHardDaysNight.txt'
  main(song_file)