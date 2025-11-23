### Documentation for piano.html

#### Overview
This file renders a layered piano keyboard using SVG. It includes visual layers for white keys, black keys, and fingering overlays. The fingering overlay is dynamically populated using JavaScript.

#### Structure
1. **HTML Head**
   - Includes metadata and inline CSS for styling the page and SVG.
   - Loads the fingeringMap.js script to handle dynamic rendering of fingering overlays.
   - Contains an inline script that calls `renderFingering` to display the fingering for the `C7` chord when the DOM is ready.

2. **SVG Layers**
   - **Layer 1: White Background**
     - A white rectangle spans the entire SVG canvas.
   - **Layer 2: Black Dividers**
     - Vertical black lines separate the white keys.
   - **Layer 3: Black Keys**
     - Black rectangles represent the sharp/flat keys.
   - **Layer 4: Fingering Overlays**
     - A `<g>` element (`#fingering-overlay`) is used to dynamically render fingering dots.

3. **Definitions**
   - A `<circle>` (`#fingering-dot`) defines the base dot for fingering.
   - A `<g>` (`#fingering-anchor`) positions the dot at a fixed vertical position.

#### Key Features
- **Dynamic Fingering Overlay**: The `renderFingering` function from fingeringMap.js populates the `#fingering-overlay` group with dots based on the selected chord.
- **Scalable Vector Graphics**: The SVG is responsive and maintains aspect ratio.

---

### Documentation for fingeringMap.js

#### Overview
This JavaScript file provides utilities for rendering fingering overlays on the piano keyboard. It maps musical notes to their corresponding positions on the keyboard and dynamically updates the SVG.

#### Functions
1. **`getFingeringX(note)`**
   - **Purpose**: Calculates the horizontal position of a note on the keyboard.
   - **Parameters**:
     - `note` (string): The musical note (e.g., `C`, `Fsharp`).
   - **Returns**:
     - The x-coordinate of the note or `null` if the note is not found.
   - **Logic**:
     - Looks up the note in `whiteKeyX` or `blackKeyX` objects.
     - Adds an offset of 30 to the x-coordinate.

2. **`renderFingering(chordName, svgGroupId)`**
   - **Purpose**: Renders fingering dots for a given chord.
   - **Parameters**:
     - `chordName` (string): The name of the chord (e.g., `C_major`, `C7`).
     - `svgGroupId` (string): The ID of the SVG group where the dots will be rendered.
   - **Logic**:
     - Clears existing dots in the target group.
     - Iterates over the notes in the chord and calculates their positions using `getFingeringX`.
     - Appends `<use>` elements to the group to display the dots.

#### Data
1. **`whiteKeyX`**
   - Maps white keys to their x-coordinates.
   - Example: `{ F: 0, G: 60, A: 120, ... }`.

2. **`blackKeyX`**
   - Maps black keys to their x-coordinates.
   - Example: `{ Fsharp: 40, Gsharp: 100, Asharp: 160, ... }`.

3. **`chords`**
   - Maps chord names to their constituent notes.
   - Example: `{ C_major: ['C', 'E', 'G'], C7: ['C', 'E', 'Asharp'] }`.

---

### Usage
1. **Add New Chords**
   - Update the `chords` object in fingeringMap.js with the new chord name and its notes.

2. **Render Fingering**
   - Call `renderFingering(chordName, svgGroupId)` with the desired chord and target SVG group ID.

3. **Customize Appearance**
   - Modify the `<circle>` definition in piano.html to change the appearance of the fingering dots.

Let me know if you need further clarification!