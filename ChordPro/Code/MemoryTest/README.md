
---

# 🎸 **ChordReveal**

A browser‑based chord‑memory tool. It steps through a song, one chord line at a time.  
It loads a simple `.txt` file containing sections, chord lines, and lyrics, plus optional metadata at the top.  
The interface supports tap, click, and keyboard stepping — including a “go back” function.  
It has a **Leading Words Mode** that shows the first two words of each lyric line alongside its chord line.

---

## ✨ Features

- Load a `.txt` song file directly from disk  
- Optional metadata block at the top of the file  
- Section detection (`[Verse 1]`, `[Chorus]`, etc.)  
- Chord‑line detection - handles leading space
- Lyric capture for “leading words” mode  
- Step forward using tap, click, Space, Enter, or →  
- Step backward using Backspace or ←  
- Clean reveal queue: section → chord lines → blank → next section  
- Solo sections automatically skipped  
- Runs entirely in the browser - no server

---

## 📄 Input File Format (`.txt`)

A song file consists of:

1. **Optional metadata block**  
2. **Sections**  
3. **Chord lines**  
4. **Lyric lines**

### 1. Metadata Block (optional)

At the top of the file:

```
#title: All My Loving
#artist: Beatles
#key-original: C
#key-me: C
#capo: 0
#tempo: 88

```

- Lines beginning with `#` are parsed as metadata  
- The metadata block ends at the first non‑empty, non‑metadata line  
- All metadata fields are optional  

### 2. Sections

Sections are declared thus:

```
[Verse 1]
[Chorus]
[Bridge]
```

- Section names are displayed during reveal  
- A section named `Solo` (case‑insensitive) is **skipped entirely**

### 3. Chord Lines

Chord lines may be indented:

```
           Em            A7          D           Bm
```

A chord line is any line where **every token** matches a chord pattern:

- Root: `A`–`G`  
- Optional accidental: `#` or `b`  
- Optional quality: `m`, `maj`, `min`, `dim`, `aug`, `sus`, `add`  
- Optional extension: digits  

Examples:

- `Em`  
- `A7`  
- `Bbmaj7`  
- `G#dim`  
- `Cadd9`  
- `%` and `|` are also accepted  

### 4. Lyric Lines

Any non‑chord, non‑section, non‑metadata line is treated as a lyric line.

Lyrics are **ignored for stepping**, but used for **Leading Words Mode**.

---

## 🎛 Leading Words Mode (default ON)

When enabled, each chord line is displayed as:

```
<first two lyric words> : <chords>
```

Example:

Input:

```
           Em            A7          D           Bm
Close your eyes and I’ll kiss you…
```

Output:

```
Close your : Em A7 D Bm
```

This mode can be toggled at runtime (default: ON).

---

## 🧠 Parsing Logic (summary)

The parser:

1. Reads metadata until the first non‑metadata line  
2. Detects section headers  
3. Skips `[Solo]` sections entirely  
4. Detects chord lines using a strict token‑based rule  
5. Associates the **next lyric line** with the **previous chord line**  
6. Builds a structure:

```js
{
  meta: { ... },
  sections: ["Verse 1", "Chorus", ...],
  sectionsWithLines: {
    "Verse 1": [
      { chords: ["Em","A7","D","Bm"], lyric: "Close your eyes..." },
      { chords: ["G","Em","C","A7"], lyric: "Remember I'll always..." },
      ...
    ],
    ...
  }
}
```

---

## ▶️ Reveal Engine

The reveal engine builds a linear queue:

```
Section header
Chord line 1
Chord line 2
(blank)
Section header
Chord line 1
...
```

Each tap/click/keypress advances one step.

Backward stepping moves one step back.

---

## ⌨️ Controls

### Forward
- **Tap** on the tap area  
- **Click** inside the tap area  
- **Space**  
- **Enter**  
- **ArrowRight**

### Backward
- **ArrowLeft**  
- **Backspace**

### Toggle Leading Words Mode
- **L** key (default ON)

---

## 🧩 Display Logic

### Section header
Displayed in `sectionDisplay`.

### Chord line
Displayed in `display`, formatted via:

```js
formatLine(entry)
```

Which returns either:

```
Em   A7   D   Bm
```

or (leading words mode):

```
Close your : Em A7 D Bm
```

---

## 🗂 File Structure

```
index.html
style.css
script.js
```

No build step.  
No server.  
Runs directly in the browser.

---

## 🚀 Extending the Tool

You can easily add:

- Auto‑transpose  
- Capo‑aware chord display  
- Full lyric mode  
- Section jump menu  
- Auto‑scroll based on tempo  
- Dark mode  

---

