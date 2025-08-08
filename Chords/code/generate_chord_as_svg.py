# Generate SVG chord diagrams from a text file containing chord definitions.
# Example of a chord definition line:
# X32010 | C Major | well known fingering for C major chord
# Entry point is the function `batch_generate_html`.

# this script generates SVG chord diagrams from a text file containing chord definitions.
# The text file should contain lines formatted as:
# chord_code | chord_name | comment (optional)
# where chord_code is a string of fret numbers and 'X' for muted strings.

import re
import html
import os

# --- Constants ---
NOTE_NAMES = ["E", "F", "F#", "G", "G#", "A", "A#", "B", "C", "C#", "D", "D#"]
STRING_ROOTS = ["E", "A", "D", "G", "B", "E"]  # Strings 6 to 1

NOTE_MAP = {note: i for i, note in enumerate(NOTE_NAMES)}

# --- Utilities ---
def note_at(string_index, fret_number):
    """Return the note name for the given string and fret."""
    root_note = STRING_ROOTS[string_index]
    root_index = NOTE_MAP[root_note]
    return NOTE_NAMES[(root_index + fret_number) % 12]

def sanitize_filename(chord_name):
    name = re.sub(r'\s+', '-', chord_name.strip())
    name = re.sub(r'[^\w\-]', '', name)
    return f"chord-{name.lower()}.html"

# --- Diagram Generators ---
def generate_fret_lines(y_fret_start=30, y_fret_increment=40, num_frets=6):
    lines = []
    for i in range(num_frets):
        y = y_fret_start + i * y_fret_increment
        x1 = 10 if i != 0 else 8
        x2 = 160 if i != 0 else 162
        lines.append(f'<line class="fret-bar" x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" />')
    return '\n'.join(lines)

def generate_string_lines(x_start=10, string_spacing=30, y_string_start=30, string_length=220, num_strings=6):
    lines = []
    for i in range(num_strings):
        x = x_start + i * string_spacing
        y1 = y_string_start
        y2 = y_string_start + string_length
        lines.append(f'<line class="string-line" x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" />')
    return '\n'.join(lines)

def generate_svg_positions(
    chord_code,
    chord_name="",
    comment="",
    x_start=10,
    string_spacing=30,
    fret_spacing=40,
    y_marker_top=25,
    y_chord_label=-2,
    dot_radius=6
):
    """Generate SVG elements for the chord diagram positions."""
    # Validate chord_code
    svg = []

    if chord_name:
        svg.append(f'<text class="fret-label" x="85" y="{y_chord_label}">{chord_name}</text>')

    if comment:
        num_strings = 6
        diagram_width = num_strings * string_spacing
        comment_x = x_start + diagram_width

        diagram_bottom_y = y_marker_top + num_strings * fret_spacing
        comment_y = diagram_bottom_y + 30

        escaped_comment = html.escape(comment)
        svg.append(f'<text class="chord-comment" x="{comment_x}" y="{comment_y}" text-anchor="right">{escaped_comment}</text>')

    for i, fret in enumerate(chord_code):
        string_index = i
        x = x_start + i * string_spacing

        if fret.upper() == "X":
            svg.append(f'<text class="string-muted" x="{x}" y="{y_marker_top}">X</text>')
        elif fret == "0":
            note = note_at(string_index, 0)
            svg.append(f'<rect class="note-box" x="{x - 8}" y="{y_marker_top - 12}" width="16" height="16" rx="2" />')
            svg.append(f'<text class="open-note" x="{x}" y="{y_marker_top}">{note}</text>')
        elif fret.isdigit():
            fret_number = int(fret)
            note = note_at(string_index, fret_number)
            y = fret_number * fret_spacing + y_marker_top - dot_radius
            svg.append(f'<circle class="dot-active" cx="{x}" cy="{y}" r="{dot_radius}" />')
            svg.append(f'<rect class="note-box" x="{x - 8}" y="{y - 22}" width="16" height="16" rx="2" />')
            svg.append(f'<text class="note-label" x="{x}" y="{y - 10}">{note}</text>')       

    return '\n'.join(svg)

# --- HTML Generator ---
def generate_full_html(chord_code, chord_name="", comment=""):
    svg_positions = generate_svg_positions(chord_code, chord_name, comment)
    fret_lines = generate_fret_lines()
    string_lines = generate_string_lines()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{chord_name} – Fretboard Diagram</title>
  <link rel="stylesheet" href="../../css/fretboard.css">
</head>
<body>
  <svg xmlns="http://www.w3.org/2000/svg"
       width="600" height="600"
       viewBox="-10 -20 500 500"
       preserveAspectRatio="xMidYMid meet"
       class="fretboard">

    <!-- inject:strings -->
{string_lines}
    <!-- END strings -->

    <!-- inject:frets -->
{fret_lines}
    <!-- END frets -->

    <!-- inject:positions -->
{svg_positions}
    <!-- END positions -->
  </svg>
</body>
</html>"""

# --- Batch Execution ---
def read_chord_definitions(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            parts = [part.strip() for part in line.split('|')]
            if len(parts) == 2:
                chord_code, chord_name = parts
                comment = ""
            elif len(parts) >= 3:
                chord_code, chord_name, comment = parts[0], parts[1], '|'.join(parts[2:])  # handles extra '|' in comment
            yield chord_code, chord_name, comment

def get_chord_root_folder(chord_name):
    """Extract the root letter (A-G) from the chord name for folder classification."""
    match = re.match(r"\s*([A-G])", chord_name.upper())
    if match:
        return match.group(1)
    return "Other"

def batch_generate_html(input_file="code/chords.txt", output_dir="svg_chord_output"):
    ensure_chord_folders(output_dir)  # 1. Ensure folders exist
    for chord_code, chord_name, comment in read_chord_definitions(input_file):
        html_output = generate_full_html(chord_code, chord_name, comment)
        root_folder = get_chord_root_folder(chord_name)
        folder_path = os.path.join(output_dir, root_folder)
        os.makedirs(folder_path, exist_ok=True)
        filename = os.path.join(folder_path, sanitize_filename(chord_name))  # 2. Save to correct folder
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html_output)
        print(f"✅ Generated: {filename}")

def ensure_chord_folders(output_dir="svg_chord_output"):
    for letter in "ABCDEFG":
        folder = os.path.join(output_dir, letter)
        os.makedirs(folder, exist_ok=True)

if __name__ == "__main__":
    batch_generate_html()

