from mido import Message, MidiFile, MidiTrack

# Constants
PPQ = 100  # ticks per beat
kick_note = 36
snare_note = 38
channel = 9

# Create MIDI file and track
mid = MidiFile(ticks_per_beat=PPQ)
track = MidiTrack()
mid.tracks.append(track)

# Kick at beat 0, lasts 1 beat
track.append(Message('note_on', note=kick_note, velocity=100, time=0, channel=channel))
track.append(Message('note_off', note=kick_note, velocity=0, time=PPQ, channel=channel))  # 1 beat later

# Snare at beat 9, lasts 2 beats
snare_start = 9 * PPQ
snare_duration = 2 * PPQ
track.append(Message('note_on', note=snare_note, velocity=100, time=snare_start - PPQ, channel=channel))  # delta from last event
track.append(Message('note_off', note=snare_note, velocity=0, time=snare_duration, channel=channel))

# Save
mid.save('kick_snare_bar2.mid')