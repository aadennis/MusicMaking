from music21 import stream
import copy
from typing import Callable, Optional


def build_and_write_example(part, example: str, out_dir: Optional[str] = r"c:/temp",
                            write_musicxml: bool = False) -> str:
    """
    Write the provided `part` to a MIDI file (and optionally MusicXML).

    This function does NOT modify the given `part` except to place it into a
    Score for writing. Pattern-building (appending notes/rests) should be done
    by the caller so the function remains generic and case-specific.

    Parameters
    - part: music21.stream.Part or stream.Score already containing events
    - example: string used to form the output filename (e.g. "01")
    - out_dir: directory to write the output file to (default: c:/temp)
    - write_musicxml: if True, also write a MusicXML file beside the MIDI file

    Returns the path to the MIDI file that was written.
    """
    midi_file = f"{out_dir}/drum_example_{example}.mid"

    # If a Score was passed in, use it directly; otherwise create a Score and
    # insert the provided Part so the file has proper structure.
    if isinstance(part, stream.Score):
        score = part
    else:
        score = stream.Score()
        score.insert(0, part)

    # Write MIDI
    score.write('midi', fp=midi_file)

    # Optionally write MusicXML for notation inspection
    if write_musicxml:
        xml_file = f"{out_dir}/drum_example_{example}.musicxml"
        score.write('musicxml', fp=xml_file)

    return midi_file
