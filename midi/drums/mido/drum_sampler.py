import random
from mido import Message, MidiFile, MidiTrack, MetaMessage, bpm2tempo
from drum_constants import *  # or import only the notes you want

# General MIDI drum range
DRUM_RANGE = range(35, 82)

# Playback settings
BPM = 68
TICKS_PER_BEAT = 480  # standard mido default
BAR_LENGTH = TICKS_PER_BEAT * 4
VELOCITY = 64  # arbitrary “average” velocity
NOTE_LENGTH = TICKS_PER_BEAT // 2  # half-beat hit

def create_drum_sampler_midi(filename="drums/midi_drum_tracks/drum_sampler.mid"):
    mid = MidiFile(type=1)
    track = MidiTrack()
    mid.tracks.append(track)
    mid.tracks.append(track)

    tempo = bpm2tempo(BPM)
    track.append(MetaMessage('set_tempo', tempo=tempo))

    current_time = 0

    for note in DRUM_RANGE:
        # Note on
        track.append(Message('note_on', channel=9, note=note, velocity=VELOCITY, time=current_time))
        # Note off after NOTE_LENGTH
        track.append(Message('note_off', channel=9, note=note, velocity=0, time=NOTE_LENGTH))
        # Wait 1 bar before next note
        current_time = BAR_LENGTH - NOTE_LENGTH  # delta time for next note_on

    mid.save(filename)
    print(f"Created drum sampler MIDI: {filename}")

if __name__ == "__main__":
    create_drum_sampler_midi()
