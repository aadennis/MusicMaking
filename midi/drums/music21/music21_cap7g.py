"""
Create a percussion sequence using the General MIDI (GM) drum map.
It demonstrates how to:
1. Use semantic drum codes instead of raw MIDI numbers
2. Create proper percussion notation that will render with drum clef
3. Ensure correct playback on MIDI channel 10 (GM drum kit channel)

Key Features:
- Uses semantic codes (e.g., "KB" for Bass Drum) instead of MIDI numbers
- Maps to standard GM drum note numbers (35-81)
- Automatically sets up proper percussion staff and MIDI channel
"""

from music21 import *
from music21.base import Music21Object
import copy
from gm_drums import GM_DRUMS, KICK_OHH, KICK, SNARE # Import drum mappings
from music21.write_example import build_and_write_example

# As this is specifically for drums, duration of a note will always be
# a quarter of a quarter, ie semantically 16th or 0.25
SIXTEENTH = duration.Duration('16th')

# Helper function to convert semantic drum codes into music21 Chord objects
# Args:
#   *codes: Variable number of drum codes (e.g., "KB", "ASN")
# Returns:
#   music21.chord.Chord object with the corresponding MIDI note numbers
# Example:
#   drum_chord("KB", "ASN") creates a chord with MIDI notes [36, 38] (kick + snare)
def drum_chord(*codes):
    c = chord.Chord([GM_DRUMS[code] for code in codes])
    c.duration = SIXTEENTH
    return c

def drum_rest(rest_count:int = 1):
    r = note.Rest()
    r.duration = duration.Duration(SIXTEENTH.quarterLength * rest_count)
    return r

"""
Insert an element into a part at a specific 16th-note slot, replacing anything already at that slot.

Parameters:
part (music21.stream.Part): the target part to modify (modified in place).
slot_index (int): zero-based slot number; the function computes offset = slot_index * SIXTEENTH.quarterLength.
element (music21.base.Music21Object): element to insert (Note, Chord, Rest, etc.). 
    The function inserts the object as given (no automatic deepcopy).

Behavior:
Computes the exact offset for the requested slot.
Removes any existing element(s) that begin exactly at that offset (uses mustBeginInSpan=True) so the new element replaces them.
Inserts the provided element at the computed offset.

Returns:
None (modifies part in-place).

Notes / tips:
Use copy.deepcopy(element) when calling this function if you want to keep the original object unchanged.
slot_index is intended to be an integer counting SIXTEENTH-sized slots; using non-integers will 
    produce fractional offsets and is not recommended.
This is a convenience helper for patterns laid out on a uniform grid of SIXTEENTH durations.
"""
def insert_at_slot(part: stream.Part, slot_index: int, element: Music21Object):
    offset = slot_index * SIXTEENTH.quarterLength
    # Remove any existing element at that offset
    for e in part.getElementsByOffset(offset, mustBeginInSpan=True):
        part.remove(e)

    part.insert(offset, element)

"""
Append a chord followed by an optional rest to a music21 Part.

Parameters:
    part (stream.Part): The target part to append to (modified in place)
    chord_obj (Music21Object): The chord to append. Will be deep copied before appending
    rest_count (int): Number of sixteenth-note rests to add after the chord. Default: 0 (no rest)

This function is designed for building rhythmic patterns by combining chords with
trailing rests. It's particularly useful for drum patterns where you want a hit
followed by a specific number of silent sixteenth notes.

Example:
    # Add a kick drum with 3 sixteenth rests after it (total duration = 1 quarter note)
    add_chord_with_rest_tail(part, kick, 3)
"""
def add_chord_with_rest_tail(part: stream.Part, chord_obj: Music21Object, rest_count: int = 0):
    part.append(copy.deepcopy(chord_obj))
    if rest_count > 0:
        part.append(drum_rest(rest_count))

# Create and configure the percussion part:
# 1. Create a Part to hold our drum sequence
# 2. Create an UnpitchedPercussion instrument (tells music21 this is a drum part)
# 3. Set MIDI channel to 9 (= channel 10 in 1-based counting) for GM drum sounds
# 4. Insert the percussion instrument at the start of the part

perc = instrument.UnpitchedPercussion()
perc.midiChannel = 9  # MIDI channel 10 (0-based index)

# Create the drum patterns using semantic codes:
# - chord1: Combines Acoustic Snare ("ASN"=38) and Low Floor Tom ("LFT"=41)
# - chord2: Single Bass Drum hit ("KB"=36)
# other usage examples:
# basic_pattern = drum_chord(*BASIC_KIT)  # All basic kit sounds
# tom_fill = drum_chord(*TOMS[:3])  # First three toms
# latin_groove = drum_chord(*LATIN[:2])  # First two Latin instruments
kick_ohh = drum_chord(*KICK_OHH) # see gm_drums.py for decode
kick = drum_chord(*KICK)
snare = drum_chord(*SNARE)
ohh = drum_chord("OHH")       

# Build the sequence and write files using the helper in write_example.py
# Restore case-specific pattern-building here (keeps write_example.py generic)
example = "01"
part = stream.Part()
part.insert(0, perc)  # Position 0 = start of part
# Bar 1
add_chord_with_rest_tail(part, kick, 3)  # Kick + 3 sixteenth rests
add_chord_with_rest_tail(part, snare, 3)  # Kick + 3 sixteenth rests
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, snare, 3) 
# Bar 2
add_chord_with_rest_tail(part, kick, 3)  # Kick + 3 sixteenth rests
add_chord_with_rest_tail(part, snare, 3)  # Kick + 3 sixteenth rests
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, snare, 3) 

# Write to MIDI file (and optionally MusicXML) using helper that only writes
# Pass the Part directly; the writer will wrap it into a Score internally.
midi_file = build_and_write_example(part, example=example)
#---

example = "02"
part = stream.Part()
part.insert(0, perc)  # Position 0 = start of part
# Bar 1
add_chord_with_rest_tail(part, kick, 3)  
add_chord_with_rest_tail(part, snare, 3) 
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, snare, 3) 
# Bar 2
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, snare, 3) 
add_chord_with_rest_tail(part, kick, 1) 
add_chord_with_rest_tail(part, kick, 1) 
add_chord_with_rest_tail(part, snare, 0) 
add_chord_with_rest_tail(part, kick, 2) 

midi_file = build_and_write_example(part, example=example)
#---
example = "03"
part = stream.Part()
part.insert(0, perc)  # Position 0 = start of part
# Bar 1
add_chord_with_rest_tail(part, kick, 3)  
add_chord_with_rest_tail(part, snare, 3) 
add_chord_with_rest_tail(part, kick, 1)
add_chord_with_rest_tail(part, kick, 1)
add_chord_with_rest_tail(part, snare, 3) 
# Bar 2
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, snare, 1) 
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, kick, 1) 
add_chord_with_rest_tail(part, snare, 3) 

midi_file = build_and_write_example(part, example=example)

#---
example = "04"
part = stream.Part()
part.insert(0, perc)  # Position 0 = start of part
# Bar 1
add_chord_with_rest_tail(part, kick, 1)  
add_chord_with_rest_tail(part, kick, 1)  
add_chord_with_rest_tail(part, snare, 1) 
add_chord_with_rest_tail(part, kick, 3) 
add_chord_with_rest_tail(part, kick, 1)  
add_chord_with_rest_tail(part, snare, 1) 
add_chord_with_rest_tail(part, kick, 3)  
# Bar 2
add_chord_with_rest_tail(part, kick, 1) 
add_chord_with_rest_tail(part, snare, 1) 
add_chord_with_rest_tail(part, kick, 1) 
add_chord_with_rest_tail(part, kick, 1)
add_chord_with_rest_tail(part, kick, 0)
add_chord_with_rest_tail(part, kick, 0)
add_chord_with_rest_tail(part, snare, 3) 

midi_file = build_and_write_example(part, example=example)