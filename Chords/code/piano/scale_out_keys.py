# Generate scaled divider lines for SVG piano scaffold
scaled_spacing = 42
height = 200
count = 11  # Number of dividers

for i in range(1, count + 1):
    x = i * scaled_spacing
    print(f'<line x1="{x}" y1="0" x2="{x}" y2="{height}" />')

print("-----------------------------")

# Generate black key positions based on scaled white key spacing
black_key_width = 28  # 70% of original 40
white_spacing = 42

# Define black key positions relative to white key gaps
# These are approximate midpoints between white keys
black_key_offsets = [1, 2, 3, 5, 6, 8, 9, 10, 12]  # Indexes between white keys

for i in black_key_offsets:
    center = i * white_spacing - (black_key_width / 2)
    print(f'<rect x="{round(center, 1)}" y="0" width="{black_key_width}" height="120" fill="black" />')    

print("-----------------------------")
white_keys = ['F-2', 'G-2', 'A-2', 'B-2', 'C-3', 'D-3', 'E-3', 'F-3', 'G-3', 'A-3', 'B-3', 'C-4']
scaled_spacing = 42

for i, key in enumerate(white_keys):
    x = i * scaled_spacing
    print(f"  '{key}': {x},")

print("-----------------------------")

black_keys = {
    'F#-2': 1, 'G#-2': 2, 'A#-2': 3,
    'C#-3': 5, 'D#-3': 6,
    'F#-3': 8, 'G#-3': 9, 'A#-3': 10,
    'C#-4': 12
}

for key, index in black_keys.items():
    center = index * scaled_spacing - 14  # 14 = half of 28px width
    print(f"  '{key}': {round(center)},")

    
