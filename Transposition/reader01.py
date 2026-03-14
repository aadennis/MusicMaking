import re

import re

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