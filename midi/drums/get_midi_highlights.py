import mido

mid = mido.MidiFile('drums/test_data/baiao1.mid')

notes = []
velocities = []
time_signatures = []
tempo = None

for track in mid.tracks:
    for msg in track:
        if msg.type == 'note_on' and msg.velocity > 0:
            notes.append(msg.note)
            velocities.append(msg.velocity)
        elif msg.type == 'time_signature':
            time_signatures.append((msg.numerator, msg.denominator))
        elif msg.type == 'set_tempo':
            tempo = msg.tempo  # microseconds per beat

# Convert tempo to BPM
bpm = mido.tempo2bpm(tempo) if tempo else None

print(f"Notes played: {sorted(set(notes))}")
print(f"Velocity range: {min(velocities)}–{max(velocities)}")
print(f"BPM: {bpm}")
print(f"Time Signatures: {time_signatures}")
