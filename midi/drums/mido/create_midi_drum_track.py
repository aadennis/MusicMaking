import random
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from drum_constants import KICK, SIDE_STICK, RIDE  # import only what you need

# Global velocity scaling factor
VEL_SCALE = 1.2

# Per-instrument scaling (multipliers)
INSTRUMENT_SCALE = {
    KICK: 1.2,        # kick a bit stronger
    SIDE_STICK: 1.0,  # natural
    RIDE: 0.8,        # keep the ride soft
}

def vel(base, instrument):
    """Scale velocity by global + per-instrument factors and clamp to 0–127."""
    scale = VEL_SCALE * INSTRUMENT_SCALE.get(instrument, 1.0)
    return max(1, min(127, int(base * scale)))

def create_cant_help_falling_midi(filename="midi_drum_tracks/cant_help_drums.mid"):
    mid = MidiFile(type=1)
    track = MidiTrack()
    mid.tracks.append(track)

    bpm = 68
    tempo = bpm2tempo(bpm)
    track.append(MetaMessage('set_tempo', tempo=tempo))

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

            # Kick + side stick
            if step == 0:
                events.append(('on', tick_time, KICK, vel(50, KICK)))
                events.append(('off', tick_time + eighth//2, KICK, 0))
            if step == 6:
                events.append(('on', tick_time, KICK, vel(40, KICK)))
                events.append(('off', tick_time + eighth//2, KICK, 0))
                events.append(('on', tick_time, SIDE_STICK, vel(25, SIDE_STICK)))
                events.append(('off', tick_time + eighth//2, SIDE_STICK, 0))

            # Ride every 8th note
            ride_base = 30 + random.randint(-3, 3)
            ride_vel = vel(ride_base, RIDE)
            events.append(('on', tick_time, RIDE, ride_vel))
            events.append(('off', tick_time + eighth//2, RIDE, 0))

    # Sort by absolute time
    events.sort(key=lambda e: e[1])

    # Convert to delta times and append to track
    last_time = 0
    for ev_type, abs_time, note, velocity in events:
        delta = abs_time - last_time
        track.append(Message('note_on' if ev_type == 'on' else 'note_off',
                             note=note, velocity=velocity, time=delta))
        last_time = abs_time

    mid.save(filename)
    print(f"Created: {filename}")

if __name__ == "__main__":
    create_cant_help_falling_midi()
