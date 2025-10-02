import re

def extract_plugins_from_rpp(rpp_path):
    with open(rpp_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Split into track blocks
    track_blocks = re.findall(r'<TRACK.*?>.*?<FXCHAIN.*?>.*?</FXCHAIN>.*?</TRACK>', content, re.DOTALL)

    results = []

    for i, block in enumerate(track_blocks, start=1):
        # Extract track name
        name_match = re.search(r'NAME\s+"([^"]+)"', block)
        track_name = name_match.group(1) if name_match else f"Track {i}"

        # Extract plugin lines
        plugin_matches = re.findall(r'<VST\s+"([^"]+)"', block)
        plugins = plugin_matches if plugin_matches else ["(No plugins found)"]

        results.append((track_name, plugins))

    return results

# Example usage
rpp_file = "reaper/Multitude_FirstLight_TuneCoreVersionVStrip3.rpp"
plugin_summary = extract_plugins_from_rpp(rpp_file)

# Print results
for track_name, plugins in plugin_summary:
    print(f"\n🎛️ {track_name}")
    for plugin in plugins:
        print(f"  - {plugin}")

