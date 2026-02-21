# ChordReveal — Developer Documentation

This document describes the internal architecture, data flow, and design principles of the ChordReveal application. It is intended for developers extending or maintaining the codebase.

---

## 1. Overview

ChordReveal is a browser‑based chord‑practice tool. It loads a `.txt` file containing:

- An optional metadata block
- Section headers
- Chord lines
- Lyric lines

The system parses the file into a structured representation, builds a linear reveal queue, and steps through the queue using tap, click, or keyboard input.

The architecture is intentionally minimal: no build step, no server, no dependencies.

---

## 2. High-Level Architecture

TXT File → Parser → Data Model → Reveal Queue → UI Renderer


### Components

| Component | Responsibility |
|----------|----------------|
| **Parser** | Reads metadata, sections, chord lines, lyric lines. Produces structured data. |
| **Data Model** | `{ meta, sections, sectionsWithLines }` |
| **Reveal Queue** | Linear list of `{type, ...}` items for stepping. |
| **Renderer** | Displays section headers and formatted chord lines. |
| **Input Layer** | Handles tap, click, and keyboard navigation. |

---

## 3. Input Format Specification

### 3.1 Metadata Block

- Appears at the top of the file.
- Lines beginning with `#` are parsed as key/value pairs.
- Ends at the first non‑empty, non‑metadata line.

Example:
#title: All My Loving #artist: Beatles #tempo: 88


### 3.2 Sections

[Verse 1] [Chorus]


- Section names are stored in order.
- A section named `Solo` (case‑insensitive) is skipped entirely.

### 3.3 Chord Lines

Chord lines may be indented. A chord line is any line where **every token** matches the chord token regex:

^A-G][#b]?(mMmajmindimaugsusadd)?\d*$


Special tokens `%` and `|` are also accepted.

### 3.4 Lyric Lines

Any non‑chord, non‑section, non‑metadata line is treated as a lyric line.

The lyric line is associated with the **most recent chord line**.

---

## 4. Data Model

The parser returns:

```js
{
  meta: { title, artist, ... },
  sections: ["Verse 1", "Chorus", ...],
  sectionsWithLines: {
    "Verse 1": [
      { chords: ["Em","A7","D","Bm"], lyric: "Close your eyes..." },
      { chords: ["G","Em","C","A7"], lyric: "Remember I'll always..." }
    ],
    ...
  }
}
```

## 5. Reveal Queue  
The reveal queue is a flattened list  

```js
[
  { type: "section", name: "Verse 1" },
  { type: "line", entry: { chords, lyric } },
  { type: "line", entry: { chords, lyric } },
  { type: "blank" },
  { type: "section", name: "Chorus" },
  ...
]
```

This ensures predictable stepping.

## 6. Rendering Logic
   
Section header
Displayed in sectionDisplay.
Chord line
Displayed in display, formatted via:

formatLine(entry)

Leading Words Mode
If enabled:
<first two lyric words> : <chords>


Otherwise:
Em   A7   D   Bm



## 7. Input Handling

Forward
- Tap on tap area
- Click on tap area
- Space
- Enter
- ArrowRight
Backward
- ArrowLeft
- Backspace
Toggle Leading Words Mode
- Key: L

## 8. Invariants
- revealIndex always points to the next item to display.
- sectionsWithLines[section] always contains objects { chords, lyric }.
- Lyric lines never affect chord detection.
- No section is ever empty unless the input file is malformed.
- Solo sections are never added to the reveal queue.

## 9. Extensibility
The architecture supports:
- Auto‑transpose
- Capo‑aware chord display
- Full lyric mode
- Auto‑scroll based on tempo
- Section jump menu
- Dark mode
The parser and reveal engine are stable and modular.

---

# 🎵 **2. Musician‑Friendly README (simple, practical)**  
### `README.md`

```markdown
# ChordReveal

ChordReveal is a simple tool that helps you practise songs one chord line at a time. Load a `.txt` file, tap to step through the chords, and keep your hands on your instrument.

No installation. No setup. Just open the page and load a song.

---

## How to Use

1. Open the app in your browser.
2. Click **Load File** and choose a `.txt` song file.
3. Tap or press **Space** to step through the song.
4. Press **←** to go back a step.
5. Press **L** to toggle “Leading Words Mode”.

---

## File Format

Your `.txt` file should look like this:

#title: All My Loving #artist: Beatles
[Verse 1] Em            A7          D           Bm Close your eyes and I'll kiss you G           Em        C     A7 Remember I'll always be true


### Metadata (optional)

Lines starting with `#` set the title, artist, key, etc.

### Sections

Use `[Verse 1]`, `[Chorus]`, etc.

### Chords

Chord lines can be indented. The app recognises:

- Em
- A7
- Bbmaj7
- G#dim
- Cadd9
- %
- |

### Lyrics

Lyrics go under the chord line. They are ignored for stepping but used for “Leading Words Mode”.

---

## Controls

### Step Forward
- Tap the screen
- Click the tap area
- Space
- Enter
- ArrowRight

### Step Backward
- ArrowLeft
- Backspace

### Toggle Leading Words Mode
- Press **L**

---

## Leading Words Mode

Shows the first two words of the lyric line before the chords:

Close your : Em A7 D Bm


This helps you remember where you are in the song.

---

## Why This Tool Exists

ChordReveal is designed for musicians who want:

- A clean, distraction‑free chord trainer
- No scrolling
- No clutter
- No complicated formats
- Just chords, sections, and a simple tap‑to‑advance flow




