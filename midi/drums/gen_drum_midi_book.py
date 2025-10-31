"""Generate a simple drum MIDI file from a hand-specified pattern.

This small script demonstrates how to build a MIDI file containing
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

from mido import MetaMessage, Message, MidiFile, MidiTrack, bpm2tempo

# Create a new MIDI file and a single track for our drum events
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Set a simple tempo: 120 beats per minute
# We also set a program change (not strictly necessary for percussion)
track.append(Message('program_change', program=0, time=0))
track.append(MetaMessage('set_tempo', tempo=bpm2tempo(120)))

# Timing constants
# `ticks_per_beat` is the MIDI file resolution (default 480 ticks/beat)
ticks_per_beat = mid.ticks_per_beat
# We subdivide each beat into 4 16th-note subdivisions (4 subdivisions per
# quarter note => 16 subdivisions per 4/4 measure)
subdivisions = 16  # 16th notes per measure
# Number of MIDI ticks that correspond to one 16th-note subdivision
ticks_per_subdivision = ticks_per_beat // 4

# Simple drum note mapping (General MIDI percussion):
# - 36: Bass Drum 1 (kick)
# - 38: Acoustic Snare
kick = 36
snare = 38
velocity = 100  # how hard the drum is hit (0-127)

# A minimal, human-readable pattern definition. Each measure is a dict
# that lists which subdivision indices (0..15) contain a kick or snare.
# Here we define two identical measures; you can add more entries to
# extend the pattern.
pattern = [
    # Measure 1
    {'kick': [0, 8], 'snare': [4, 12]},
    # Measure 2
    {'kick': [0, 8], 'snare': [4, 12]},
]


def append_hit(note: int, vel: int, duration_ticks: int):
    """Append a note_on followed by a note_off after duration_ticks.

    We use a pair of Message objects with the note_on having time=0 and the
    subsequent note_off carrying the time delta to advance the track.
    """
    track.append(Message('note_on', note=note, velocity=vel, time=0))
    track.append(Message('note_off', note=note, velocity=0, time=duration_ticks))


# Build MIDI events from the pattern. For each subdivision in each measure
# we either add a kick hit, a snare hit, or advance time when there is no hit.
for measure in pattern:
    for i in range(subdivisions):
        # duration to advance after a hit (or to advance when no hit)
        time = ticks_per_subdivision

        if i in measure.get('kick', []):
            # Add a bass drum hit at this subdivision
            append_hit(kick, velocity, time)
        elif i in measure.get('snare', []):
            # Add a snare hit at this subdivision
            append_hit(snare, velocity, time)
        else:
            # No drum hit on this subdivision. We still need to advance
            # the MIDI time; using a note_off with note=0 is a simple way
            # to emit a delta-time-only event with mido.
            track.append(Message('note_off', note=0, velocity=0, time=time))


# Write the constructed MIDI file to disk
mid.save('drum_pattern.mid')
