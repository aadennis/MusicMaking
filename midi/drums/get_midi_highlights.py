import pretty_midi
import os

# Input and output filenames
input_file = 'drums/test_data/baiao1.mid'
output_file = 'midi_features_output.txt'

# Load and analyze MIDI
pm = pretty_midi.PrettyMIDI(input_file)

note_numbers = [note.pitch for instrument in pm.instruments for note in instrument.notes]
velocities = [note.velocity for instrument in pm.instruments for note in instrument.notes]
bpm = pm.estimate_tempo()
time_signature_changes = [(ts.numerator, ts.denominator) for ts in pm.time_signature_changes]

# Prepare output text
output_text = f"""🎼 MIDI Feature Summary
Input File: {input_file}
Output File: {output_file}

Notes Played: {sorted(set(note_numbers))}
Velocity Range: {min(velocities)}–{max(velocities)}
Estimated BPM: {round(bpm, 2)}
Time Signatures: {time_signature_changes}
"""

# Write to file
with open(output_file, 'w') as f:
    f.write(output_text)

print(f"Features written to {output_file}")