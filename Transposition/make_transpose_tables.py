#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, List

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

# Canonical sharp pitch classes (this is the *output* spelling)
PC_SHARPS: List[str] = ["C", "C#", "D", "D#", "E", "F",
                        "F#", "G", "G#", "A", "A#", "B"]

# Optional: canonical flat pitch classes (alternative output spelling)
PC_FLATS: List[str]  = ["C", "Db", "D", "Eb", "E", "F",
                        "Gb", "G", "Ab", "A", "Bb", "B"]

# Optional: hybrid of sharps plus Bb (alternative output spelling)
PC_HYBRID: List[str] = ["C", "C#", "D", "D#", "E", "F",
                        "F#", "G", "G#", "A", "Bb", "B"]

# Range of allowed offsets (inclusive)
MIN_OFFSET, MAX_OFFSET = -3, 3

# Toggle if you also want to generate flat-spelled output files
GENERATE_FLATS = False  # set True to generate the _flats.* files as well
GENERATE_HYBRID = True

# Output file names
CSV_SHARPS = Path("transpose_lookup.csv")
CSV_FLATS  = Path("transpose_lookup_flats.csv")
CSV_HYBRID  = Path("transpose_lookup_hybrid.csv")

JSON_SHARPS = Path("transpose_lookup.json")
JSON_FLATS = Path("transpose_lookup_flats.json")
JSON_HYBRID = Path("transpose_lookup_hybrid.json")

# ----------------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------------

def build_table(pitch_classes: List[str]) -> Dict[str, Dict[int, str]]:
    """
    Build a nested mapping:
        table[root][k] = transposed_note
    where 'root' and 'transposed_note' both come from 'pitch_classes',
    and k is a semitone offset in [MIN_OFFSET..MAX_OFFSET].
    """
    index = {pc: i for i, pc in enumerate(pitch_classes)}
    table: Dict[str, Dict[int, str]] = {}

    for root in pitch_classes:
        i0 = index[root]
        row: Dict[int, str] = {}
        for k in range(MIN_OFFSET, MAX_OFFSET + 1):
            row[k] = pitch_classes[(i0 + k) % 12]
        table[root] = row

    return table


def write_csv(table: Dict[str, Dict[int, str]], path: Path) -> None:
    """
    Write a tall CSV with columns: source, offset, target
    """
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "offset", "target"])
        for src, mapping in table.items():
            for k in range(MIN_OFFSET, MAX_OFFSET + 1):
                w.writerow([src, k, mapping[k]])


def write_json(table: Dict[str, Dict[int, str]], path: Path) -> None:
    """
    Write a nested JSON object:
        { "C": {"-3":"A", ..., "3":"D#"}, ... }
    with stable key order (by source then offset).
    """
    # Convert int keys to str for JSON
    out = {src: {str(k): tgt for k, tgt in sorted(mapping.items())}
           for src, mapping in table.items()}
    with path.open("w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)


# ----------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------

def main() -> None:
    # Sharp-spelled outputs
    sharp_table = build_table(PC_SHARPS)
    write_csv(sharp_table, CSV_SHARPS)
    write_json(sharp_table, JSON_SHARPS)
    print(f"Wrote {CSV_SHARPS} and {JSON_SHARPS}")

    # Optional: flat-spelled outputs
    if GENERATE_FLATS:
        flat_table = build_table(PC_FLATS)
        write_csv(flat_table, CSV_FLATS)
        write_json(flat_table, JSON_FLATS)
        print(f"Wrote {CSV_FLATS} and {JSON_FLATS}")

    # Optional: hybrid-spelled outputs
    if GENERATE_HYBRID:
        hybrid_table = build_table(PC_HYBRID)
        write_csv(hybrid_table, CSV_HYBRID)
        write_json(hybrid_table, JSON_HYBRID)
        print(f"Wrote {CSV_HYBRID} and {JSON_HYBRID}")

if __name__ == "__main__":
    main()