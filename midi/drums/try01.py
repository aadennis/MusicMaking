from music21 import *
import copy

chord1 = chord.Chord([36,41])
chord2 = chord.Chord([38])
rest = note.Rest()
stream1 = stream.Stream()

for i in range(2):
    stream1.append(copy.deepcopy(chord1))
    stream1.append(copy.deepcopy(chord2))
    stream1.append(copy.deepcopy(rest))

stream1.write('midi', fp="c:/temp/mahtest.mid")

print('xxxxxx')