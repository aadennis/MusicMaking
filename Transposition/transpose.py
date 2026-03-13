import json
import pandas as pd
from io import StringIO


REQUIRED_COLS = ["transposition", "from_chord", "to_chord"]

def to_normalised_json(
        df: pd.DataFrame, *,
        as_str: bool = False,
        indent: int | None = 2,
        sort_groups: bool = True,
):
    df = df.copy()
    for c in REQUIRED_COLS:
        df[c] = df[c].astype(str).str.strip()
    df = df[(df["transposition"] != "") & (df["from_chord"] != "") & (df["to_chord"] != "")]
  
    groups = []
    for name, g in df.groupby("transposition", sort=sort_groups):
        rows = g[["from_chord", "to_chord"]].reset_index(drop=True).to_dict(orient="records")
        groups.append({"name": name, "rows": rows})

    if sort_groups:
        groups.sort(key=lambda x: x["name"])

    if as_str:
        return json.dumps(groups, ensure_ascii=False, indent=indent)
    return groups


csv_text = """transposition,from_chord,to_chord
C-D,C,D
C-D,F,G
C-D,Em,F#M
C-D,G9,A9
C-D,G7,A7
G-F,G,F
G-F,C,A#
G-F,F,D#
G-F,D,C
G-F,Bm,Am
G-F,Em,Dm
G-F,C6,A#6
G-F,D7sus4,C7sus4
G-F,Dm7,Cm7
"""

def doit():
    df = pd.read_csv(StringIO(csv_text))
    json_str = to_normalised_json(df, as_str=True, indent=2)
    print(json_str)

if __name__ == '__main__':
    doit()