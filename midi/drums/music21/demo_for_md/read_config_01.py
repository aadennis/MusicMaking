from json import load
from music21 import meter, tempo, stream, note
from pandas import read_csv

def get_config_data():
    with open('music21/demo_for_md/read_config_01.json','r') as f:
        config = load(f)
    return config["bpm"], config["quarterLength"], config["TimeSignature"]


def insert_note(stream_obj, midi_data_row, quarterLength, index):
    velocity = midi_data_row['Velocity']
    if velocity == 0:
        return  # Skip inserting notes with zero velocity
    n = note.Note()
    n.volume.velocity = velocity
    
    n.pitch.midi = midi_data_row['Note']
    n.quarterLength = quarterLength
    n.volume.velocity = midi_data_row['Velocity']

    offset = quarterLength * index
    stream_obj.insert(offset, n)

def insert_note_set(midi_data, stream_obj):
    for i, row in midi_data.iterrows():
        insert_note(stream_obj, row, quarterLength_config, i)

# main()...

bpm_config, quarterLength_config, ts_config = get_config_data()
ts = meter.TimeSignature(ts_config)
mm = tempo.MetronomeMark(number=bpm_config)

drum_stream = stream.Stream()
drum_stream.insert(0.0, ts)
drum_stream.insert(0.0, mm)

midi_data_kick = read_csv('music21/demo_for_md/demo_kick.csv')
insert_note_set(midi_data_kick, drum_stream)

midi_data_snare = read_csv('music21/demo_for_md/demo_snare.csv')
insert_note_set(midi_data_snare, drum_stream)

drum_stream.write('midi', fp="c:/temp/demo_10.mid")
    
