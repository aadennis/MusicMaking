import json
from pathlib import Path

# Load configuration from a JSON file
# The configuration file contains layout settings and chord details
with open("code/chord_config.json") as f:
    config = json.load(f)

# Start building the HTML content with the header
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Chord Layout</title>
  <!-- Link to external CSS for fretboard styling -->
  <link rel="stylesheet" href="css/fretboard.css">
  <style>
    /* Style for the container wrapping all chords */
    .chord-wrapper {{
      display: flex;
      flex-wrap: wrap;
      gap: {config['layout']['gap']}; /* Gap between chord elements */
      padding: 20px; /* Padding around the container */
    }}
    /* Style for individual fretboard elements */
    .fretboard {{
      width: {config['layout']['width']}; /* Width of each fretboard */
      height: {config['layout']['height']}; /* Height of each fretboard */
      border: 1px solid #ccc; /* Border around each fretboard */
    }}
  </style>
</head>
<body>
  <!-- Container for all chord SVGs -->
  <div class="chord-wrapper">
"""

# Loop through each chord in the configuration
# Read the SVG content from the file and inject it into the HTML
for chord in config["chords"]:
    svg_content = Path(chord["file"]).read_text()  # Read the SVG file content
    html += f"\n<!-- {chord['label']} -->\n{svg_content}\n"  # Add a comment with the chord label and the SVG content

# Close the HTML structure
html += """
  </div>
</body>
</html>
"""

# Save the generated HTML content to a file
Path("chords_layout.html").write_text(html)