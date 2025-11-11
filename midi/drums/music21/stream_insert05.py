"""
MIDI Drum Pattern Generator with CSV Import Support

This module creates MIDI drum patterns by reading pattern data from CSV files and
generating a music21 stream with proper timing and velocity control. It supports:
1. Reading separate patterns for different drum elements (e.g., main pattern and hi-hat)
2. Precise timing control with triplet-based positioning
3. Velocity control for dynamic expression
4. Time signature and tempo settings

Required CSV Format:
- stream_insert05.csv: Main pattern with columns 'Note' (MIDI note number) and 'Velocity'
- hihat_144beats.csv: Hi-hat pattern with same column structure

Dependencies:
    music21: For MIDI and musical structure handling
    pandas: For CSV file reading and data management
"""

from music21 import stream, meter, tempo, note
import pandas as pd

# Initialize main stream with time signature and tempo
s1 = stream.Stream()
ts = meter.TimeSignature('4/4')
mm = tempo.MetronomeMark(number=79)  # Set tempo to 79 BPM
s1.insert(0.0, ts)
s1.insert(0.0, mm)

# Load pattern data from CSV files
midi_set = pd.read_csv('midi_in_plain_text/stream_insert05.csv')
hihat_midi_set = pd.read_csv('midi_in_plain_text/hihat_144beats.csv')

# Debug print of main pattern notes
for i,row in midi_set.iterrows():
    print(row['Note'])

def insert_note(stream_obj, midi_note, velocity, offset):
    """
    Insert a note into a music21 stream with precise timing and velocity control.

    Args:
        stream_obj (music21.stream.Stream): The target stream to insert into
        midi_note (int): MIDI note number (35-81 for GM drum kit)
        velocity (int): MIDI velocity (0-127)
        offset (float): Position in the stream (in triplet units)

    Note:
        - Uses triplet-based timing (quarterLength = 1/3)
        - Offset is converted to triplet position (offset / 3)
        - Origin is fixed at 0.0 but could be parameterized if needed
    
    Example:
        >>> s = stream.Stream()
        >>> insert_note(s, 36, 80, 0)  # Insert bass drum at start
        >>> insert_note(s, 42, 60, 1)  # Insert hi-hat 1 triplet later
    """
    origin = 0.0
    n = note.Note()
    n.pitch.midi = midi_note
    n.quarterLength = 1/3  # Triplet timing
    n.volume.velocity = velocity
    stream_obj.insert(origin + (offset / 3), n)


# Generate main drum pattern
# Iterates through the main pattern CSV, inserting notes sequentially
# Each note is positioned one triplet after the previous
offset = 0
for i, row in midi_set.iterrows():
    insert_note(s1, row['Note'], row['Velocity'], offset)
    offset += 1

# Generate hi-hat pattern
# Similar to main pattern but uses separate CSV file for hi-hat specific pattern
# This allows for independent hi-hat patterns that can be modified separately
offset = 0
for i, row in hihat_midi_set.iterrows():
    insert_note(s1, row['Note'], row['Velocity'], offset)
    offset += 1

# Write the complete pattern to a MIDI file
# The resulting file combines both the main pattern and hi-hat pattern
# with proper timing and velocity information
s1.write('midi', fp="c:/temp/stream_with_hihat01.mid")

print('MIDI file generated successfully with both main pattern and hi-hat')
