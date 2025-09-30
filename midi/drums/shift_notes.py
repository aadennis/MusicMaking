from mido import MidiFile, MidiTrack

def shift_notes(input_file, output_file, shifts):
    """
    Shift specified MIDI notes by N semitones.

    Parameters:
    - input_file: str, path to the original MIDI file
    - output_file: str, path to save the modified MIDI
    - shifts: dict, keys are MIDI note numbers to shift, values are semitone shifts
              e.g., {36: 1, 38: -1} will shift C1 up 1 semitone and D1 down 1 semitone
    """
    midi = MidiFile(input_file)
    new_midi = MidiFile()

    for track in midi.tracks:
        new_track = MidiTrack()
        for msg in track:
            if msg.type in ('note_on', 'note_off') and msg.note in shifts:
                new_note = msg.note + shifts[msg.note]
                # Ensure note stays in valid MIDI range 0–127
                msg.note = max(0, min(127, new_note))
            new_track.append(msg)
        new_midi.tracks.append(new_track)

    new_midi.save(output_file)


# Example usage: shift C1 up 1 semitone, D1 down 1 semitone
shift_notes('drums/test_data/baiaox.mid', 'drums_shiftedx.mid', {36: 1, 38: -1})
