from json import load

with open('music21/demo_for_md/read_config_01.json','r') as f:
    configData = load(f)

bpm = configData.get("bpm")
quarterLength = configData.get("quarterLength")
ts = configData.get("TimeSignature")



