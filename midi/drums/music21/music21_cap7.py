from music21 import *
# https://www.music21.org/music21docs/usersGuide/usersGuide_07_chords.html
cMinor = chord.Chord(["C4","G4","E-5"])
# Now try a drum, as these do not get mentioned...
mahDrum = chord.Chord([36,38,41]) # kick, snare, tom
print(cMinor.pitches)
print(mahDrum.pitches)
#cMinor.show()
mahDrum.write('midi',fp="c:/temp/x.mid")
# The above writes out a single chord fine, but say I have a chord (by
# default these are quarter-notes), then a rest, then a chord then a rest
stream1 = stream.Stream()
stream1.append(mahDrum)
mahDrum = chord.Chord([36]) # kick, snare, tom
stream1.append(mahDrum)
mahDrum = chord.Chord([36,38,41]) # kick, snare, tom
r = note.Rest()
stream1.append(r)