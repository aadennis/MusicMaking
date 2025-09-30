import mido
from collections import defaultdict

input_file = 'drums/test_data/erkwel2_100_6-8_36189.mid'
output_file = 'mido_note_velocity_summary.txt'

mid = mido.MidiFile(input_file)

# Track velocities per note
note_velocities = defaultdict(list)
time_signatures = []
tempo = None

for track in mid.tracks:
    for msg in track:
        if msg.type == 'note_on' and msg.velocity > 0:
            note_velocities[msg.note].append(msg.velocity)
        elif msg.type == 'time_signature':
            time_signatures.append((msg.numerator, msg.denominator))
        elif msg.type == 'set_tempo':
            tempo = msg.tempo

# Convert tempo to BPM
bpm = mido.tempo2bpm(tempo) if tempo else None

# Prepare output
summary_lines = [
    f"MIDI Summary (via mido)",
    f"Input File: {input_file}",
    f"Output File: {output_file}",
    "",
    f"Estimated BPM: {round(bpm, 2) if bpm else 'Unknown'}",
    f"Time Signatures: {time_signatures}",
    "",
    "Note Velocity Ranges:"
]

for note in sorted(note_velocities):
    velocities = note_velocities[note]
    summary_lines.append(f"  Note {note}: min={min(velocities)}, max={max(velocities)}")

# Write to file
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(summary_lines))

print(f"Summary written to {output_file}")