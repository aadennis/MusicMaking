import os
import random
from mido import MidiFile, MidiTrack, MetaMessage, tempo2bpm

def extract_metadata(mid):
    bpm = None
    ts = None
    for track in mid.tracks:
        for msg in track:
            if msg.type == 'set_tempo' and bpm is None:
                bpm = round(tempo2bpm(msg.tempo))
            elif msg.type == 'time_signature' and ts is None:
                ts = (msg.numerator, msg.denominator)
            if bpm and ts:
                break
    return bpm or 120, ts or (4, 4)

def patch_and_rename(input_path, override_bpm=None, override_ts=None):
    mid = MidiFile(input_path)
    mid.type = 1  # Ensure multi-track format

    # Extract original metadata
    bpm, (numerator, denominator) = extract_metadata(mid)

    # Apply overrides if provided
    if override_bpm is not None:
        bpm = override_bpm
    if override_ts is not None:
        numerator, denominator = override_ts

    # Strip existing time_signature events
    for track in mid.tracks:
        track[:] = [msg for msg in track if msg.type != 'time_signature']

    # Inject clean time signature at tick 0
    ts_track = MidiTrack()
    ts_track.append(MetaMessage('time_signature', numerator=numerator, denominator=denominator, time=0))
    mid.tracks.insert(0, ts_track)

    # Build output filename
    base, ext = os.path.splitext(os.path.basename(input_path))
    suffix = random.randint(10000, 99999)
    output_name = f"{base}_{bpm}_{numerator}-{denominator}_{suffix}{ext}"
    output_path = os.path.join(os.path.dirname(input_path), output_name)

    mid.save(output_path)
    print(f"Saved: {output_path}")

def main():
    input_file = 'drums/test_data/erkwel2.mid'

    # Optional overrides
    override_bpm = None           # e.g. 100 or None
    override_ts = (6,8)           # e.g. (6, 8) or None

    patch_and_rename(input_file, override_bpm, override_ts)

if __name__ == "__main__":
    main()

