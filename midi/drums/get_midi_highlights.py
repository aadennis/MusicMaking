import mido
from mido import MidiFile, tempo2bpm

input_file = 'drums/test_data/baiao1.mid'
output_file = 'mido_summary.txt'

mid = MidiFile(input_file)

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
            tempo = msg.tempo

bpm = tempo2bpm(tempo) if tempo else None

summary = f"""MIDI Summary (via mido)
Input File: {input_file}
Output File: {output_file}

Notes Played: {sorted(set(notes))}
Velocity Range: {min(velocities)}–{max(velocities)}
Estimated BPM: {round(bpm, 2) if bpm else 'Unknown'}
Time Signatures: {time_signatures}
"""

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(summary)

print(f"Summary written to {output_file}")
