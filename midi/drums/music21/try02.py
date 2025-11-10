from music21 import *
import copy

def append_sequence(stream_obj, sequence):
    """
    Append a sequence of music21 objects (chords or rests) to a stream.
    
    Args:
        stream_obj: A music21 Stream object to append to
        sequence: List of music21 objects (Chords or Rests)
    """
    for item in sequence:
        stream_obj.append(copy.deepcopy(item))
    return stream_obj

# Define your basic elements
chord1 = chord.Chord([36,41])  # Bass drum + Low floor tom
chord2 = chord.Chord([38])     # Acoustic snare
rest = note.Rest()

# Create the stream
stream1 = stream.Stream()

# Define the pattern as a list of elements
pattern = [chord1, chord2, rest]

# Repeat the pattern twice
for i in range(2):
    append_sequence(stream1, pattern)

# Write to MIDI file
stream1.write('midi', fp="c:/temp/mahtest.mid")

print('Pattern written to MIDI file')