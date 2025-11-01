from music21 import note, stream
s = stream.Stream()

c4 = note.Note('C4')
c5 = note.Note('C5')

s.append(c4)
s.append(c5)

s.show()



