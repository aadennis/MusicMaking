from music21 import stream, meter, tempo, note

s1 = stream.Stream()
ts = meter.TimeSignature('4/4')
mm = tempo.MetronomeMark(number=79)
s1.insert(0.0, ts)
s1.insert(0.0, mm)
s1.insert(0.0, note.Note(midi=36, quarterLength=1))
s1.insert(1.0, note.Note(midi=38, quarterLength=1))
s1.insert(2.0, note.Note(midi=42, quarterLength=1))
s1.insert(3.0, note.Note(midi=46, quarterLength=1))


s1.write('midi', fp="c:/temp/stream_insert01.mid")