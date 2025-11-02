'''
    Create a drum score consisting of a small number of quarternotes, these being the default.
    This is a simple showcase for Music21.
    See readme cap7 for fuller description.
'''

from music21 import *
import copy

part = stream.Part()                       # Use a Part for clear instrument assignment
perc = instrument.UnpitchedPercussion()    # Create percussion instrument
perc.midiChannel = 9                       # Set to channel 10 (0-indexed)
part.insert(0, perc)                       # Add instrument to part
# part.insert(0, clef.PercussionClef())

chord1 = chord.Chord([38, 41])  # snare (38), low floor tom (41)
chord2 = chord.Chord([36])      # kick (36)

# append independent copies
part.append(copy.deepcopy(chord1))
part.append(copy.deepcopy(chord2))
part.append(copy.deepcopy(chord1))
part.append(note.Rest())
part.append(copy.deepcopy(chord1))

# create score and add part
score = stream.Score()
score.insert(0, part)
# score.show()

score.write('midi', fp=r"c:/temp/x3.mid")