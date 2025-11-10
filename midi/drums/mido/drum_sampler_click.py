import random
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from drum_constants import KICK, SNARE, HIHAT_CLOSED

DRUM_RANGE = range(35, 82)
BPM = 68
TICKS_PER_BEAT = 480
BAR_LENGTH = TICKS_PER_BEAT * 4
VELOCITY_CLICK = 50
VELOCITY_TARGET = 64
NOTE_LENGTH = TICKS_PER_BEAT // 4

def create_drum_sampler_with_click(filename="drums/midi_drum_tracks/drum_sampler_click.mid"):
    mid = MidiFile(type=1)
    track = MidiTrack()
    mid.tracks.append(track)

    tempo = bpm2tempo(BPM)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    abs_time = 0  # absolute time counter

    for target_note in DRUM_RANGE:
        bar_start = abs_time
        events = []

        # Click track: 8 steps (eighth notes)
        for step in range(8):
            tick_time = bar_start + step * (TICKS_PER_BEAT // 2)

            # Kick on beat 1
            if step % 4 == 0:
                events.append(('on', tick_time, KICK, VELOCITY_CLICK))
                events.append(('off', tick_time + NOTE_LENGTH, KICK, 0))
            # Snare on beat 3
            if step % 4 == 2:
                events.append(('on', tick_time, SNARE, VELOCITY_CLICK))
                events.append(('off', tick_time + NOTE_LENGTH, SNARE, 0))
            # Hi-hat every 8th
            events.append(('on', tick_time, HIHAT_CLOSED, VELOCITY_CLICK))
            events.append(('off', tick_time + NOTE_LENGTH, HIHAT_CLOSED, 0))

        # Add target note on beat 1
        events.append(('on', bar_start, target_note, VELOCITY_TARGET))
        events.append(('off', bar_start + NOTE_LENGTH, target_note, 0))

        # Sort events by absolute time
        events.sort(key=lambda e: e[1])

        # Convert absolute times to deltas
        last_time = abs_time
        for ev_type, event_time, note, vel in events:
            delta = event_time - last_time
            track.append(Message('note_on' if ev_type == 'on' else 'note_off',
                                 channel=9, note=note, velocity=vel, time=delta))
            last_time = event_time

        # Move abs_time to next bar
        abs_time = bar_start + BAR_LENGTH

    mid.save(filename)
    print(f"Created drum sampler with click track: {filename}")

if __name__ == "__main__":
    create_drum_sampler_with_click()
