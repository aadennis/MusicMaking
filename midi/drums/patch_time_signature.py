from mido import MidiFile, MidiTrack, MetaMessage
import os
import random
import sys

def patch_time_signature(input_path, numerator=6, denominator=8):
    # Load the MIDI file
    mid = MidiFile(input_path)

    # Convert to type 1 to allow multiple tracks
    mid.type = 1

    # Create a new track with the time signature
    ts_track = MidiTrack()
    ts_track.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator, time=0))

    # Insert the time signature track at the beginning
    mid.tracks.insert(0, ts_track)

    # Generate output filename with random suffix
    base, ext = os.path.splitext(input_path)
    suffix = random.randint(10000, 99999)
    output_path = f"{base}_patched_{suffix}{ext}"

    # Save the patched MIDI
    mid.save(output_path)
    print(f"Saved patched MIDI to: {output_path}")

def main():
    input_file = 'drums/test_data/erkwel2.mid'
    patch_time_signature(input_file)

if __name__ == "__main__":
    main()