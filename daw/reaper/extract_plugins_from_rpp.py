import re

def extract_plugins_from_rpp(rpp_path):
    with open(rpp_path, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()

    results = []
    current_track = None
    current_plugins = []
    inside_fxchain = False
    inside_vst_block = False
    vst_name = None

    for line in lines:
        line = line.strip()

        # Detect start of a new track
        if line.startswith("<TRACK"):
            if current_track:
                results.append((current_track, current_plugins))
            current_track = "Unnamed Track"
            current_plugins = []
            inside_fxchain = False
            inside_vst_block = False
            vst_name = None

        # Extract track name
        elif line.startswith("NAME") and current_track == "Unnamed Track":
            match = re.match(r'NAME\s+"(.+)"', line)
            if match:
                current_track = match.group(1)

        # Detect FXCHAIN block
        elif line.startswith("<FXCHAIN"):
            inside_fxchain = True

        elif line.startswith(">") and inside_fxchain and not inside_vst_block:
            inside_fxchain = False

        # Detect start of VST block
        elif inside_fxchain and line.startswith("<VST"):
            vst_match = re.match(r'<VST\s+"([^"]+)"', line)
            if vst_match:
                vst_name = vst_match.group(1)
                inside_vst_block = True

        # Detect end of VST block
        elif inside_vst_block and line == ">":
            if vst_name:
                current_plugins.append(vst_name)
            vst_name = None
            inside_vst_block = False

    # Append last track
    if current_track:
        results.append((current_track, current_plugins))

    return results

# Example usage
rpp_file = "reaper/Multitude_FirstLight_TuneCoreVersionVStrip3.rpp"
plugin_summary = extract_plugins_from_rpp(rpp_file)

# Print results
for track_name, plugins in plugin_summary:
    print(f"\nTrack name: [{track_name}]")
    for plugin in plugins:
        print(f"  - {plugin}")