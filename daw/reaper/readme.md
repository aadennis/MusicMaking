# Reaper Management

#### tested on Reaper 7.x

# Scripts


## Python

### extract_plugins_from_rpp.py

## Overview

This Python script extracts plugin information from a REAPER `.rpp` project file. It identifies the tracks and the associated VST plugins used in the project, providing a summary of the plugins for each track.

## Features

- Parses REAPER `.rpp` project files.
- Extracts track names and associated VST plugins.
- Outputs a summary of tracks and their plugins.

## Requirements

- Python 3.6 or higher.

## Usage

1. Place the `.rpp` file you want to analyze in the same directory as the script or provide the correct path.
2. Update the `rpp_file` variable in the script with the path to your `.rpp` file.
3. Run the script:

   ```bash
   python extract_plugins_from_rpp.py
   ```

4. The script will output the track names and their associated plugins to the console.

## Example Output

```plaintext
Track name: [Track 1]
  - Plugin 1
  - Plugin 2

Track name: [Track 2]
  - Plugin 3
```

## How It Works

1. **File Parsing**: The script reads the `.rpp` file line by line.
2. **Track Detection**: It identifies the start of a new track using the `<TRACK` tag.
3. **Plugin Extraction**: Within each track, it looks for `<FXCHAIN` blocks and extracts VST plugin names from `<VST` tags.
4. **Output**: The results are stored in a list and printed to the console.

## Limitations

- The script assumes the `.rpp` file is properly formatted.
- Only VST plugins are currently supported.

todo...

Lua scripting

insertKontaktMidiReady.lua

InsertLeanKontakt.lua


## License for the DAW/Reaper project

These scripts are provided as-is under the [Apache License 2.0](../LICENSE).

## Author

This script is part of the `MusicMaking` project.

