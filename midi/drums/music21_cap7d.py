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
from gm_drums import GM_DRUMS, BASIC_KIT, TOMS, CYMBALS, LATIN  # Import drum mappings

# Helper function to convert semantic drum codes into music21 Chord objects
# Args:
#   *codes: Variable number of drum codes (e.g., "BD1", "ASN")
# Returns:
#   music21.chord.Chord object with the corresponding MIDI note numbers
# Example:
#   drum_chord("BD1", "ASN") creates a chord with MIDI notes [36, 38] (kick + snare)
def drum_chord(*codes):
    return chord.Chord([GM_DRUMS[code] for code in codes])

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
chord1 = drum_chord("ASN", "LFT")  # Acoustic Snare + Low Floor Tom
chord2 = drum_chord("BD1")         # Bass Drum 1

# Build the sequence (each event is a quarter note by default):
# 1. Snare+Tom
# 2. Kick
# 3. Snare+Tom
# 4. Rest (quarter note)
# 5. Snare+Tom
# Note: deepcopy ensures each hit is an independent object
part.append(copy.deepcopy(chord1))  # Quarter note: Snare + Tom
part.append(copy.deepcopy(chord2))  # Quarter note: Kick
part.append(copy.deepcopy(chord1))  # Quarter note: Snare + Tom
part.append(note.Rest())           # Quarter note rest
part.append(copy.deepcopy(chord1))  # Quarter note: Snare + Tom

# Create a Score (container for all parts) and add our drum part
score = stream.Score()
score.insert(0, part)

# Write to MIDI file:
# - Events will be on MIDI channel 10 (GM drum channel)
# - Each note number will trigger the corresponding GM drum sound
# - To hear: Open in a DAW or player that supports GM drum sounds
score.write('midi', fp=r"c:/temp/x5.mid")

# Optional: You can also write to MusicXML to see proper drum notation:
# score.write('musicxml', fp=r"c:/temp/x4.musicxml")