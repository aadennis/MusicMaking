from music21 import stream, meter, tempo, note
import pandas as pd

s1 = stream.Stream()
ts = meter.TimeSignature('4/4')
mm = tempo.MetronomeMark(number=79)
s1.insert(0.0, ts)
s1.insert(0.0, mm)

midi_set = pd.read_csv('stream_insert05.csv')
hihat_midi_set = pd.read_csv('hihat_144beats.csv')


for i,row in midi_set.iterrows():
    print(row['Note'])

def insert_note(stream_obj, midi_note, velocity, offset):
    origin = 0.0
    n = note.Note()
    n.pitch.midi = midi_note
    n.quarterLength = 1/3
    n.volume.velocity = velocity
    stream_obj.insert(origin + (offset / 3), n)


# All notes/drums other than HiHat...
offset = 0
for i, row in midi_set.iterrows():
    insert_note(s1, row['Note'], row['Velocity'], offset)
    offset += 1

# Just HiHat...
offset = 0
for i, row in hihat_midi_set.iterrows():
    insert_note(s1, row['Note'], row['Velocity'], offset)
    offset += 1


s1.write('midi', fp="c:/temp/stream_with_hihat01.mid")
