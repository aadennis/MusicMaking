import random
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo

def create_cant_help_falling_midi(filename="drums/midi_drum_tracks/cant_help_drums.mid"):
    mid = MidiFile(type=1)
    track = MidiTrack()
    mid.tracks.append(track)

    bpm = 68
    tempo = bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    # Drum note numbers
    KICK = 36
    SNARE = 37  # side-stick
    RIDE = 51   # ride cymbal (42 = closed hi-hat alternative)

    ticks_per_beat = mid.ticks_per_beat  # usually 480
    eighth = ticks_per_beat // 2
    bar_length = eighth * 12
    total_bars = 8

    # Collect all events with absolute times
    events = []

    for bar in range(total_bars):
        bar_start = bar * bar_length
        for step in range(12):
            tick_time = bar_start + step * eighth
            # Small timing humanization
            tick_time = max(bar_start, tick_time + random.randint(-10, 10))

            # Kick + snare
            if step == 0:
                events.append(('on', tick_time, KICK, 50))
                events.append(('off', tick_time + eighth//2, KICK, 0))
            if step == 6:
                events.append(('on', tick_time, KICK, 40))
                events.append(('off', tick_time + eighth//2, KICK, 0))
                events.append(('on', tick_time, SNARE, 25))
                events.append(('off', tick_time + eighth//2, SNARE, 0))

            # Ride every 8th note
            ride_vel = max(20, min(40, 30 + random.randint(-3, 3)))
            events.append(('on', tick_time, RIDE, ride_vel))
            events.append(('off', tick_time + eighth//2, RIDE, 0))

    # Sort by absolute time
    events.sort(key=lambda e: e[1])

    # Convert to delta times and append to track
    last_time = 0
    for ev_type, abs_time, note, vel in events:
        delta = abs_time - last_time
        track.append(Message('note_on' if ev_type == 'on' else 'note_off',
                             note=note, velocity=vel, time=delta))
        last_time = abs_time

    mid.save(filename)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_cant_help_falling_midi()
