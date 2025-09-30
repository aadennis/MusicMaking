# gm_drum_reference.py
# Prints MIDI note number, Ableton Live note label, and GM drum name

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# General MIDI drum map (subset 35–81)
GM_DRUMS = {
    35: "Acoustic Bass Drum",
    36: "Bass Drum 1",
    37: "Side Stick",
    38: "Acoustic Snare",
    39: "Hand Clap",
    40: "Electric Snare",
    41: "Low Floor Tom",
    42: "Closed Hi-Hat",
    43: "High Floor Tom",
    44: "Pedal Hi-Hat",
    45: "Low Tom",
    46: "Open Hi-Hat",
    47: "Low-Mid Tom",
    48: "High-Mid Tom",
    49: "Crash Cymbal 1",
    50: "High Tom",
    51: "Ride Cymbal 1",
    52: "Chinese Cymbal",
    53: "Ride Bell",
    54: "Tambourine",
    55: "Splash Cymbal",
    56: "Cowbell",
    57: "Crash Cymbal 2",
    58: "Vibraslap",
    59: "Ride Cymbal 2",
    60: "High Bongo",
    61: "Low Bongo",
    62: "Mute High Conga",
    63: "Open High Conga",
    64: "Low Conga",
    65: "High Timbale",
    66: "Low Timbale",
    67: "High Agogo",
    68: "Low Agogo",
    69: "Cabasa",
    70: "Maracas",
    71: "Short Whistle",
    72: "Long Whistle",
    73: "Short Guiro",
    74: "Long Guiro",
    75: "Claves",
    76: "High Wood Block",
    77: "Low Wood Block",
    78: "Mute Cuica",
    79: "Open Cuica",
    80: "Mute Triangle",
    81: "Open Triangle",
}

def midi_to_ableton_name(n: int) -> str:
    """Convert MIDI note number to Ableton-style note label."""
    name = NOTE_NAMES[n % 12]
    octave = (n // 12) - 2  # Ableton offset (C3 = MIDI 60)
    return f"{name}{octave}"

if __name__ == "__main__":
    print(f"{'MIDI':>4} | {'Live':>4} | GM Drum Name")
    print("-" * 35)
    for note in range(35, 82):
        live_label = midi_to_ableton_name(note)
        gm_name = GM_DRUMS.get(note, "")
        print(f"{note:3}  | {live_label:>4} | {gm_name}")

