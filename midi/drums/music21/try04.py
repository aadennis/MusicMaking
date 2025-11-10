from music21 import *
import copy

def create_note_with_velocity(midi_note, velocity=64):
    """
    Create a note with specified velocity.
    
    Args:
        midi_note: MIDI note number
        velocity: MIDI velocity (0-127), default is 64 (half max)
    """
    n = note.Note(midi_note)
    n.volume.velocity = velocity
    return n

def create_chord_with_velocity(midi_notes, velocity=64):
    """
    Create a chord with specified velocity for all notes.
    
    Args:
        midi_notes: List of MIDI note numbers
        velocity: MIDI velocity (0-127), default is 64 (half max)
    """
    c = chord.Chord(midi_notes)
    for n in c:
        n.volume.velocity = velocity
    return c

def append_sequence(stream_obj, sequence):
    """
    Append a sequence of music21 objects (chords, notes, or rests) to a stream.
    
    Args:
        stream_obj: A music21 Stream object to append to
        sequence: List of music21 objects (Chords or Notes or Rests)
    """
    for item in sequence:
        stream_obj.append(copy.deepcopy(item))
    return stream_obj

# Define your basic elements with different velocities
note1 = create_note_with_velocity(36, velocity=80)  # Bass drum - stronger
chord1 = create_chord_with_velocity([38], velocity=64)  # Snare - medium
rest = note.Rest()

# Create the stream
stream1 = stream.Stream()

# Define the pattern as a list of elements
pattern = [chord1, note1, rest, note1]

append_sequence(stream1, pattern)

# Write to MIDI file
stream1.write('midi', fp="c:/temp/mahtest4.mid")

print('Pattern written to MIDI file with velocities: Bass=80, Snare=64')