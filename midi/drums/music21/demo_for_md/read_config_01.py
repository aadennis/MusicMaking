from json import load
from music21 import meter, tempo, stream, note
from pandas import read_csv

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

midi_data = read_csv('music21/demo_for_md/demo_kick.csv')
for i, row in midi_data.iterrows():
    print(f"Note: {row['Note']}, Velocity: {row['Velocity']}")  

