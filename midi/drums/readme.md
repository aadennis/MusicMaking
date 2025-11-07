# MIDI Drum Pattern Tools

This repository contains multiple tools for creating MIDI drum patterns:

1. [Create MIDI Drum Track](#create-midi-drum-track)
2. [Velocity-Controlled Pattern Generator](#velocity-controlled-pattern-generator)

# Velocity-Controlled Pattern Generator

A Python toolkit for creating MIDI drum patterns with precise velocity control using `music21`. This tool provides utilities for creating dynamic drum patterns with control over timing, velocity, and pattern sequencing.

## Features

- Create drum patterns using MIDI note numbers
- Control note velocity (dynamics) for each drum hit
- Flexible pattern sequencing with notes, chords, and rests
- Support for pattern repetition
- MIDI channel 10 (GM drum kit) compatibility

## API Reference

### `create_note_with_velocity(midi_note, velocity=64)`
Creates a single note with specified velocity.
- `midi_note`: MIDI note number (e.g., 36 for bass drum)
- `velocity`: MIDI velocity (0-127, default=64)

### `create_chord_with_velocity(midi_notes, velocity=64)`
Creates a chord (multiple simultaneous notes) with specified velocity.
- `midi_notes`: List of MIDI note numbers
- `velocity`: MIDI velocity (0-127, default=64)

### `append_sequence(stream_obj, sequence)`
Appends a sequence of musical elements to a stream.
- `stream_obj`: music21 Stream to append to
- `sequence`: List of notes, chords, or rests

## Example Usage

```python
from music21 import *
import copy

# Create notes/chords with velocity control
kick = create_note_with_velocity(36, velocity=80)  # Bass drum - strong
snare = create_chord_with_velocity([38], velocity=64)  # Snare - medium
hihat = create_note_with_velocity(42, velocity=50)  # Hi-hat - soft
rest = note.Rest()

# Define and play pattern
pattern = [kick, hihat, snare, hihat]
stream1 = stream.Stream()
append_sequence(stream1, pattern)
stream1.write('midi', fp="output.mid")
```

## Velocity Guidelines

- 40-50: Very soft hits
- 64: Medium volume (default)
- 80-90: Strong accents
- 100-127: Very strong hits

---

# Create MIDI Drum Track
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

Whilst the generated MIDI file can be opened in any MIDI editor, it would be more typically dragged into a DAW (in
my case Ableton Live), for further tweaking.

## License


This script is provided as-is under the MIT License.

