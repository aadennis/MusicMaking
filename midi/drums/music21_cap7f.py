"""
Create a percussion sequence using the General MIDI (GM) drum map.
It demonstrates how to:
1. Use semantic drum codes instead of raw MIDI numbers
2. Create proper percussion notation that will render with drum clef
3. Ensure correct playback on MIDI channel 10 (GM drum kit channel)

Key Features:
- Uses semantic codes (e.g., "BD1" for Bass Drum) instead of MIDI numbers
- Maps to standard GM drum note numbers (35-81)
- Automatically sets up proper percussion staff and MIDI channel
"""

from music21 import *
import copy
from gm_drums import GM_DRUMS, KICK_OHH, KICK # Import drum mappings

# As this is specifically for drums, duration of a note will always be
# a quarter of a quarter, ie semantically 16th or 0.25
SIXTEENTH = duration.Duration('16th')

# Helper function to convert semantic drum codes into music21 Chord objects
# Args:
#   *codes: Variable number of drum codes (e.g., "BD1", "ASN")
# Returns:
#   music21.chord.Chord object with the corresponding MIDI note numbers
# Example:
#   drum_chord("BD1", "ASN") creates a chord with MIDI notes [36, 38] (kick + snare)
def drum_chord(*codes):
    c = chord.Chord([GM_DRUMS[code] for code in codes])
    c.duration = SIXTEENTH
    return c

def drum_rest(rest_count:int = 1):
    r = note.Rest()
    r.duration = duration.Duration(SIXTEENTH.quarterLength * rest_count)
    return r

# Create and configure the percussion part:
# 1. Create a Part to hold our drum sequence
# 2. Create an UnpitchedPercussion instrument (tells music21 this is a drum part)
# 3. Set MIDI channel to 9 (= channel 10 in 1-based counting) for GM drum sounds
# 4. Insert the percussion instrument at the start of the part
part = stream.Part()
perc = instrument.UnpitchedPercussion()
perc.midiChannel = 9  # MIDI channel 10 (0-based index)
part.insert(0, perc)  # Position 0 = start of part

# Create the drum patterns using semantic codes:
# - chord1: Combines Acoustic Snare ("ASN"=38) and Low Floor Tom ("LFT"=41)
# - chord2: Single Bass Drum hit ("BD1"=36)
# other usage examples:
# basic_pattern = drum_chord(*BASIC_KIT)  # All basic kit sounds
# tom_fill = drum_chord(*TOMS[:3])  # First three toms
# latin_groove = drum_chord(*LATIN[:2])  # First two Latin instruments
kick_ohh = drum_chord(*KICK_OHH) # see gm_drums.py for decode
kick = drum_chord(*KICK)
ohh = drum_chord("OHH")       

# Build the sequence (each event is a quarter note by default):
# Note: deepcopy ensures each hit is an independent object
example = "01"
for i in range(8): # Example 01
    part.append(copy.deepcopy(kick)) 
    part.append(drum_rest(3))
midi_file = f"c:/temp/drum_example_{example}.mid"

# Create a Score (container for all parts) and add our drum part
score = stream.Score()
score.insert(0, part)

# Write to MIDI file:
# - Events will be on MIDI channel 10 (GM drum channel)
# - Each note number will trigger the corresponding GM drum sound
# - To hear: Open in a DAW or player that supports GM drum sounds
score.write('midi', fp=midi_file)

# Optional: You can also write to MusicXML to see proper drum notation:
# score.write('musicxml', fp=r"c:/temp/x4.musicxml")