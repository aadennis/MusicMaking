import re
from typing import Dict, Tuple

# ---- configuration ----
# Canonical pitch classes we’ll accept as roots/bass (input), with normalized output in sharps.
_PC_SHARP = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
# Map enharmonic spellings to sharp canonical forms (input normalization).
_ENHARMONIC_TO_SHARP = {
    "C": "C", "B#": "C",
    "C#": "C#", "Db": "C#", "D♭": "C#", "C♯": "C#", 
    "D": "D",
    "D#": "D#", "Eb": "D#", "E♭": "D#", "D♯": "D#",
    "E": "E", "Fb": "E", "F♭": "E",
    "F": "F", "E#": "F", "E♯": "F",
    "F#": "F#", "Gb": "F#", "G♭": "F#", "F♯": "F#",
    "G": "G",
    "G#": "G#", "Ab": "G#", "A♭": "G#", "G♯": "G#",
    "A": "A",
    "A#": "A#", "Bb": "A#", "B♭": "A#", "A♯": "A#",
    "B": "B", "Cb": "B", "C♭": "B",
}

# ---- generate transposition table for offsets –3..+3 ----
# Key: (normalized_sharp, offset)  Value: transposed_sharp
_TRANSPOSITION: Dict[Tuple[str, int], str] = {}
_index = {pc: i for i, pc in enumerate(_PC_SHARP)}

for pc in _PC_SHARP:
    i0 = _index[pc]
    for k in range(-3, 4):  # inclusive –3..+3
        _TRANSPOSITION[(pc, k)] = _PC_SHARP[(i0 + k) % 12]

# ---- chord tokenizer: root + optional accidental, suffix (no slash), optional /bass ----
_CHORD = re.compile(
    r"""
    (?P<root>[A-Ga-g])(?P<acc>[#b♯♭]?)     # root + accidental
    (?P<qual>[^/\s]*)                      # quality/suffix (stops at slash or whitespace)
    (?:/
        (?P<bass>[A-Ga-g])(?P<bacc>[#b♯♭]?) # optional slash-bass
    )?
    """,
    re.VERBOSE,
)

def _norm(note_letter: str, acc: str) -> str:
    """Normalize an input note to sharp canonical spelling (e.g., 'Db' -> 'C#')."""
    s = (note_letter.upper() + acc.replace("♯", "#").replace("♭", "b"))
    return _ENHARMONIC_TO_SHARP.get(s, s)  # if odd spellings appear, fall back as-is

def _transpose_canonical(norm_sharp: str, k: int) -> str:
    """Look up transposed note from the prebuilt table (k must be –3..+3)."""
    try:
        return _TRANSPOSITION[(norm_sharp, k)]
    except KeyError:
        raise ValueError(f"tone_offset {k} out of supported range –3..+3")

def alter_chord(chord_line: str, tone_offset: int | str) -> str:
    """
    Transpose each chord token in 'chord_line' by tone_offset semitones, using a
    precomputed lookup for offsets –3..+3. Whitespace/layout is preserved.

    Examples:
        alter_chord("    Dm7     C      Emaj7", -1)
        -> "    C#m7     B      D#maj7"
    """
    # parse/validate offset
    k = int(str(tone_offset).strip())
    if k < -3 or k > 3:
        raise ValueError("tone_offset must be within –3..+3 for the table-driven version")

    def _repl(m: re.Match) -> str:
        root = _transpose_canonical(_norm(m.group("root"), m.group("acc") or ""), k)
        qual = m.group("qual") or ""
        if m.group("bass"):
            bass = _transpose_canonical(_norm(m.group("bass"), m.group("bacc") or ""), k)
            return f"{root}{qual}/{bass}"
        return f"{root}{qual}"

    return _CHORD.sub(_repl, chord_line)