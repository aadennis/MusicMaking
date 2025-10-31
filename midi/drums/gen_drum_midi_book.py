
"""
Generate a simple drum MIDI file from a named pattern in an external JSON file.

Usage:
        python gen_drum_midi_book.py <pattern_name>

Load drum patterns from 'drum_patterns.json' (in the same directory),
where each pattern is keyed by name (e.g., 'drumpattern01'). The user must specify
the pattern name as a required argument. The output MIDI file will be named
<pattern_name>.mid.

The script furthermore demonstrates how to build a MIDI file containing
kick and snare hits arranged on 16th-note subdivisions. It uses
the `mido` library to create messages and save the resulting
MIDI file as `drum_pattern.mid`.

High-level behavior:
 - Creates a single-track MIDI file
 - Sets tempo to 120 BPM
 - Interprets a list of measures where each measure specifies
   which subdivisions get a kick or snare
 - Emits note_on / note_off pairs for hits; when there's no hit
   a zero-note off message advances the time.

This file is intentionally small and educational; it focuses on
demonstrating event timing and basic drum mapping rather than
producing a polished drum groove.
"""


import sys
import json
import os
from mido import MetaMessage, Message, MidiFile, MidiTrack, bpm2tempo

def load_pattern(pattern_name, json_path):
    """Load the specified pattern from the JSON file."""
    with open(json_path, 'r', encoding='utf-8') as f:
        patterns = json.load(f)
    if pattern_name not in patterns:
        raise ValueError(f"Pattern '{pattern_name}' not found in {json_path}. Available: {list(patterns.keys())}")
    # Convert all from 1-based to 0-based
    pattern = patterns[pattern_name]
    converted = []
    for measure in pattern:
        new_measure = {}
        for drum, hits in measure.items():
            # Only process lists, just in case
            if isinstance(hits, list):
                new_measure[drum] = [i-1 for i in hits]
            else:
                new_measure[drum] = hits
        converted.append(new_measure)
    return converted


def main():
    # if len(sys.argv) != 2:
    #     print("Usage: python gen_drum_midi_book.py <pattern_name>")
    #     sys.exit(1)
    pattern_name = 'drumpattern_test01' #sys.argv[1]
    json_path = os.path.join(os.path.dirname(__file__), 'drum_patterns.json') 
    pattern = load_pattern(pattern_name, json_path)

    # Create a new MIDI file and a single track for our drum events
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)

    # Set a simple tempo: 120 beats per minute
    # We also set a program change (not strictly necessary for percussion)
    track.append(Message('program_change', program=0, time=0))
    track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))

    # Timing constants
    ticks_per_beat = mid.ticks_per_beat
    subdivisions = 16  # 16th notes per measure
    ticks_per_subdivision = ticks_per_beat // 4

    # Simple drum note mapping (General MIDI percussion):
    # - 36: Bass Drum 1 (kick)
    # - 38: Acoustic Snare
    # - 53: Ride Bell  / Ride (cup)
    kick = 36
    snare = 38
    ridecup = 53
    velocity = 100  # how hard the drum is hit (0-127)

    def append_hit(note: int, vel: int, duration_ticks: int):
        track.append(Message('note_on', note=note, velocity=vel, time=0))
        track.append(Message('note_off', note=note, velocity=0, time=duration_ticks))

    # Build MIDI events from the pattern
    for measure in pattern:
        for i in range(subdivisions):
            time = ticks_per_subdivision
            if i in measure.get('kick', []):
                append_hit(kick, velocity, time)
            elif i in measure.get('snare', []):
                append_hit(snare, velocity, time)
            elif i in measure.get('ridecup', []):
                append_hit(ridecup, velocity, time)
                
            else:
                track.append(Message('note_off', note=0, velocity=0, time=time))

    # Write the constructed MIDI file to disk
    out_name = f"{pattern_name}.mid"
    mid.save(out_name)
    print(f"Saved MIDI file: {out_name}")


if __name__ == "__main__":
    main()


