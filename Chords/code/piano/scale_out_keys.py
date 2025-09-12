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