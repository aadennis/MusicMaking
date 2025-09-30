# create_midi_drum_track.py
## Create MIDI Drum Track

This Python script generates a MIDI drum track for the song "Can't Help Falling in Love" and saves it as a `.mid` file. The generated MIDI file includes a simple drum pattern with kick, snare, and ride cymbal.

## Features

- Generates a MIDI drum track with a tempo of 68 BPM.
- Includes humanized timing for a more natural feel.
- Uses kick, snare (side-stick), and ride cymbal sounds.
- Saves the generated MIDI file to `drums/midi_drum_tracks/cant_help_drums.mid`.

## Requirements

The script requires the following Python packages:

- `mido==1.3.3`
- `packaging==25.0`
- `python-rtmidi==1.5.8`

Install the dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Usage

Run the script directly to generate the MIDI file:

```bash
python drums/create_midi_drum_track.py
```

The generated file will be saved at `drums/midi_drum_tracks/cant_help_drums.mid`.

## How It Works

1. **Tempo and Timing**: The script sets the tempo to 68 BPM and calculates timing for eighth notes and bars.
2. **Drum Pattern**: 
   - Kick drum plays on the first and seventh eighth notes of each bar.
   - Snare drum plays alongside the kick on the seventh eighth note.
   - Ride cymbal plays on every eighth note.
3. **Humanization**: Adds slight random variations to the timing for a more natural feel.
4. **MIDI File Creation**: The events are sorted, converted to delta times, and written to a MIDI file.

## File Structure

- `create_midi_drum_track.py`: The script to generate the MIDI file.
- `drums/midi_drum_tracks/cant_help_drums.mid`: The output MIDI file.
- `requirements.txt`: Lists the required Python packages.

## Example Output

The generated MIDI file can be opened in any MIDI editor or played using a MIDI player to hear the drum pattern.

## License


This script is provided as-is under the MIT License.
