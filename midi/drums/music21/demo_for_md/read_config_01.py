from json import load

print("music21 config settings:")
with open('music21/demo_for_md/read_config_01.json','r') as f:
    configData = load(f)

print(configData)

bpm = configData.get("bpm")
quarterLength = configData.get("quarterLength")

