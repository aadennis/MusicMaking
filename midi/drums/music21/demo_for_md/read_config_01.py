from json import load
from music21 import meter, tempo

with open('music21/demo_for_md/read_config_01.json','r') as f:
    configData = load(f)

bpm_config = configData.get("bpm")
quarterLength_config = configData.get("quarterLength")
ts_config = configData.get("TimeSignature")

ts = meter.TimeSignature(ts_config)
mm = tempo.MetronomeMark(number=bpm_config)
print(f"Time Signature: {ts_config}, BPM: {bpm_config}, quarterLength: {quarterLength_config}")

