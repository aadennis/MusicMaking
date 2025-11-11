from json import load
from music21 import meter, tempo, stream, note
from pandas import read_csv

def insert_note(stream_obj, midi_data_row, quarterLength, index):
    offset = quarterLength * index
    n = note.Note()
    n.pitch.midi = midi_data_row['Note']
    n.quarterLength = quarterLength
    n.volume.velocity = midi_data_row['Velocity']
    stream_obj.insert(offset, n)

drum_stream = stream.Stream()

with open('music21/demo_for_md/read_config_01.json','r') as f:
    configData = load(f)

bpm_config = configData.get("bpm")
quarterLength_config = configData.get("quarterLength")
ts_config = configData.get("TimeSignature")

ts = meter.TimeSignature(ts_config)
mm = tempo.MetronomeMark(number=bpm_config)
drum_stream.insert(0.0, ts)
drum_stream.insert(0.0, mm)

midi_data_kick = read_csv('music21/demo_for_md/demo_kick.csv')
for i, row in midi_data_kick.iterrows():
    insert_note(drum_stream, row, quarterLength_config, i)

# that was kick. Do it all again for the snare...
midi_data_snare = read_csv('music21/demo_for_md/demo_snare.csv')
for i, row in midi_data_snare.iterrows():
    insert_note(drum_stream, row, quarterLength_config, i)

drum_stream.write('midi', fp="c:/temp/demo_05.mid")
    
