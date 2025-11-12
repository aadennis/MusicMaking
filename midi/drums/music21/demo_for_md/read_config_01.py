"""Utilities to build a simple drum stream from CSV and JSON configuration.

This module reads tempo/metric configuration from a JSON file and reads
per-instrument CSV files with 'Note' and 'Velocity' columns to populate a
music21 Stream. It exposes small helper functions used by the script-style
bottom section that writes a MIDI file.

Expected files (relative paths):
- music21/demo_for_md/read_config_01.json -- contains keys: "bpm", "quarterLength", "TimeSignature"
- music21/demo_for_md/demo_kick.csv -- CSV with columns: Note, Velocity
- music21/demo_for_md/demo_snare.csv -- CSV with columns: Note, Velocity

The functions are intentionally small and focused so they can be imported and
reused in other scripts or tests.
"""

from json import load
from music21 import meter, tempo, stream, note
from pandas import read_csv
import drum_constants as dc

def get_config_data():
    """
    Read JSON configuration and return core timing values.

    Reads the JSON file at 'music21/demo_for_md/read_config_01.json' and
    extracts the keys "bpm", "quarterLength", and "TimeSignature".

    Returns:
        tuple: (bpm, quarterLength, TimeSignature) where
            - bpm (int or float): tempo in beats per minute
            - quarterLength (float): the duration of a single grid step in quarterLength units
            - TimeSignature (str): a time signature string (e.g. '4/4')

    Raises:
        FileNotFoundError: if the JSON file does not exist
        KeyError: if any of the expected keys are missing from the JSON

    Example:
        >>> bpm, ql, ts = get_config_data()
    """
    with open('music21/demo_for_md/read_config_01.json','r') as f:
        config = load(f)
    return config["bpm"], config["quarterLength"], config["TimeSignature"]


def insert_note(stream_obj, midi_note, midi_data_row, quarterLength, index):
    """
    Insert a single note into the provided music21 stream.

    Parameters:
        stream_obj (music21.stream.Stream): Stream to insert the generated note into.
        midi_data_row (pandas.Series): A row from a CSV with the key and single value
             'Velocity' (0-127).
        quarterLength (float): Duration to assign to the created note (in
            music21 quarterLength units).
        index (int): Grid index; the function computes the insertion offset as
            `offset = quarterLength * index`.

    Behavior:
        - If the row's Velocity is 0 the function returns without inserting
          anything (interpreted as a silent/unused slot).
        - Creates a music21.note.Note, sets its MIDI pitch, duration and
          velocity, then inserts it into `stream_obj` at the computed offset.

    Returns:
        None. The stream is modified in-place.

    Example:
        >>> insert_note(my_stream, {'Note':36, 'Velocity':80}, 0.25, 4)
        # Inserts a bass-drum hit at offset 1.0 (0.25 * 4)
    """
    velocity = midi_data_row['Velocity']
    if velocity == 0:
        return  # Skip inserting notes with zero velocity
    n = note.Note()
    n.volume.velocity = velocity
    
    n.pitch.midi = midi_note
    n.quarterLength = quarterLength
    n.volume.velocity = midi_data_row['Velocity']

    offset = quarterLength * index
    stream_obj.insert(offset, n)

def insert_note_set(midi_note, midi_data, stream_obj):
    """
    Insert a sequence of notes (from a pandas DataFrame) into a stream.

    Parameters:
        midi_data (pandas.DataFrame): DataFrame where each row contains 'Note'
            and 'Velocity' columns. Rows are processed in their iteration order.
        stream_obj (music21.stream.Stream): Target stream that will be populated.

    Notes:
        - This helper relies on the module-level variable `quarterLength_config`
          to determine the duration and grid spacing of inserted notes. The
          function will call `insert_note` for each row, passing the current
          row index as the grid position.

    Returns:
        None. The provided stream is modified in-place.

    Example:
        >>> insert_note_set(midi_note, midi_df, drum_stream)
    """
    for i, row in midi_data.iterrows():
        insert_note(stream_obj, midi_note, row, quarterLength_config, i)

# main()...

bpm_config, quarterLength_config, ts_config = get_config_data()
ts = meter.TimeSignature(ts_config)
mm = tempo.MetronomeMark(number=bpm_config)

drum_stream = stream.Stream()
drum_stream.insert(0.0, ts)
drum_stream.insert(0.0, mm)

midi_data_kick = read_csv('music21/demo_for_md/8note-altrest-template01.csv')
insert_note_set(dc.KICK, midi_data_kick, drum_stream)

midi_data_snare = read_csv('music21/demo_for_md/8note-template01.csv')
insert_note_set(dc.SNARE, midi_data_snare, drum_stream)

drum_stream.write('midi', fp="c:/temp/demo_10.mid")
    
