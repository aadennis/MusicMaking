import json
from pathlib import Path

# Load config
with open("code/chord_config.json") as f:
    config = json.load(f)

# HTML header
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Chord Layout</title>
  <link rel="stylesheet" href="css/fretboard.css">
  <style>
    .chord-wrapper {{
      display: flex;
      flex-wrap: wrap;
      gap: {config['layout']['gap']};
      padding: 20px;
    }}
    .fretboard {{
      width: {config['layout']['width']};
      height: {config['layout']['height']};
      border: 1px solid #ccc;
    }}
  </style>
</head>
<body>
  <div class="chord-wrapper">
"""

# Inject SVGs
for chord in config["chords"]:
    svg_content = Path(chord["file"]).read_text()
    html += f"\n<!-- {chord['label']} -->\n{svg_content}\n"

# Close HTML
html += """
  </div>
</body>
</html>
"""

# Save output
Path("chords_layout.html").write_text(html)