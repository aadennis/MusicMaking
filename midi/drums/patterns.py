import re

# patterns.py

snares = "5-S,13-S,21-S,29-S,"

patterns = {
    "pattern01": "1-K,9-K,17-K,25-K",
    "pattern02": "1-K,9-K,17-K,25-K,27-K,30-K",
    "pattern03": "1-K,9-K,11-K,17-K,23-K,27-K",
    "pattern04": "1-K,3-K,7-K,11-K,15-K,19-K,23-K,25-K,27-K,28-K",
    "pattern05": "1-K,3-K,7-K,9-K,12-K,15-K,18-K,20-K,23-K,25-K,27-K,31-K",
    "pattern06": "1-K,9-K,15-K,17-K,19-K,20-K,23-K,25-K,27-K,31-K",
    "pattern07": "1-K,3-K,4-K,7-K,9-K,12-K,15-K,19-K,20-K,23-K,24-K,26-K,28-K,31-K",
    "pattern08": "1-K,3-K,9-K,11-K,17-K,19-K,23-K,27-K",
    "pattern09": "1-K,9-K,15-K,19-K,23-K,25-K",
    "pattern10": "1-K,9-K,17-K,19-K,23-K,27-K",
    "pattern11": "1-K,7-K,8-K,9-K,11-K,15-K,19-K,20-K,23-K,25-K,27-K,31-K",
    "pattern12": "1-K,3-K,7-K,11-K,15-K,17-K,19-K,23-K,27-K,32-K",
    "pattern13": "1-K,7-K,11-K,19-K,25-K,27-K",
    "pattern14": "1-K,9-K,17-K,25-K,27-K,30-K",
    "pattern14b": "1-K,9-K,17-K,25-K,27-K,30-K,1-Q,5-Q,9-Q,13-Q,17-Q,21-Q,25-Q",
    "patternHiHatDemo": "1-K,3-C,5-K,7-P,9-K,11-C,13-S,15-Q,17-K,19-C,21-S,23-O,25-K,27-P,29-S,31-C"
}

# MIDI Notes Definition (including Q for quarter-open hi-hat)
MIDI_NOTES = {
    'K': (36, 80),   # Kick
    'S': (38, 80),   # Snare
    'P': (44, 80),   # Pedal Hi-Hat
    'C': (42, 80),   # Closed Hi-Hat
    'Q': (46, 60),   # Quarter-Open Hi-Hat (lower velocity)
    'O': (46, 100),  # Open Hi-Hat (higher velocity)
}

# Function to parse and retrieve pattern with snares
def get_pattern_with_snares(pattern_id):
    if pattern_id not in patterns:
        raise ValueError(f"Pattern '{pattern_id}' not found.")

    pattern = snares + patterns[pattern_id]
    print(f"Full pattern for '{pattern_id}': {pattern}")  # Debugging: Show the full pattern

    # Parse the pattern and print out the details for debugging
    step_map = {}  # step: list of (midi_pitch, velocity)
    for token in pattern.split(','):
        if '-' not in token:
            continue
        step_str, instrs = token.strip().split('-')
        step = int(step_str.strip()) - 1  # 1-based to 0-based

        # Match instruments with optional velocity, e.g. K100 or just S
        entries = re.findall(r'([KSQCO])(\d{1,3})?', instrs.strip().upper())
        note_data = []
        for symbol, vel_str in entries:
            pitch, default_vel = MIDI_NOTES.get(symbol, (None, 80))  # Default to velocity 80 if missing
            if pitch is None:
                continue  # Skip if we get an unknown symbol
            velocity = int(vel_str) if vel_str else default_vel
            note_data.append((pitch, velocity))

            # Debugging: Check if Q (quarter-open hi-hat) is being parsed correctly
            if symbol == 'Q':
                print(f"DEBUG: Quarter-open hi-hat (Q) at step {step + 1} with velocity {velocity}")

        # Ensure we're adding to the correct step, and not overwriting
        if step in step_map:
            step_map[step].extend(note_data)  # Add to existing notes on that step
        else:
            step_map[step] = note_data  # First time seeing this step

    # Debugging: Check final step_map to ensure 'Q' is being included
    print(f"DEBUG: Final step_map for '{pattern_id}': {step_map}")

    return step_map

# Example of calling the function for debugging
pattern_id = "pattern14b"
pattern_with_snares = get_pattern_with_snares(pattern_id)

