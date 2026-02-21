# 🎼 **ChordReveal — Design Rationale**  
### `DESIGN-RATIONALE.md`

This document explains the architectural decisions behind ChordReveal.  
It is not a user guide or API reference — it is the “why” behind the system.

---

# 1. **Guiding Principles**

ChordReveal is built around a few core principles:

### **1.1 Zero friction**
The tool must load instantly in any browser, with:

- no build step  
- no server  
- no dependencies  
- no bundler  
- no transpiler  

This constraint eliminates CORS issues, simplifies deployment, and ensures the tool is usable on any machine, including offline laptops in rehearsal rooms.

### **1.2 Predictable stepping**
The musician must always know what will appear next:

- Section header  
- Chord line  
- Chord line  
- Blank  
- Next section  

No surprises. No skipped lines. No hidden state.

### **1.3 TXT-first workflow**
The musician’s source material is a simple `.txt` file:

- easy to edit  
- easy to generate  
- easy to version-control  
- easy to read on its own  

No ChordPro complexity. No markup. No curly braces.

### **1.4 Lyrics are optional context, not structure**
Lyrics should:

- never affect chord detection  
- never break stepping  
- never require alignment logic  

But they *can* enrich the display (e.g., Leading Words Mode).

### **1.5 Minimal cognitive load**
The UI must show:

- where you are (section)  
- what to play (chords)  
- optionally: where in the lyric you are (leading words)  

Nothing else.

---

# 2. **Why the Parser Works the Way It Does**

### **2.1 Metadata block at the top**
Metadata is placed at the top because:

- it avoids mixing metadata with musical content  
- it avoids ChordPro parsing complexity  
- it is trivial to generate programmatically  
- it is trivial to ignore if missing  

The parser stops reading metadata at the first non‑empty, non‑metadata line.  
This keeps the rule simple and predictable.

### **2.2 Section headers use `[Section Name]`**
This is:

- human‑readable  
- visually distinct  
- unambiguous  
- easy to detect with a single condition  

Skipping `[Solo]` is a deliberate design choice:  
musicians rarely need to practise solos in this stepping format.

### **2.3 Chord detection is token‑based**
Chord lines are detected by checking **every token** against a chord regex.

This avoids:

- false positives from lyrics  
- reliance on indentation  
- reliance on alternating chord/lyric patterns  
- brittle heuristics  

The regex is intentionally conservative — better to reject a malformed chord than misclassify a lyric.

### **2.4 Lyric lines are stored but never drive logic**
Lyrics are captured only to support Leading Words Mode.

They never:

- toggle state  
- affect chord detection  
- influence stepping  

This keeps the parser robust even with messy input.

---

# 3. **Why the Reveal Engine Is Linear**

### **3.1 Flattening the structure**
Instead of stepping through nested structures (sections → lines), the system flattens everything into a single `revealQueue`.

This has major benefits:

- stepping forward/backward is trivial  
- no nested indices  
- no special cases  
- no “end of section” logic  
- no off‑by‑one errors  

The queue is the single source of truth for the UI.

### **3.2 Blank lines between sections**
A blank item between sections:

- gives the musician a visual breath  
- prevents cognitive blending of sections  
- makes backward stepping clearer  

This is a UX decision, not a parsing one.

---

# 4. **Why Leading Words Mode Exists**

Musicians often remember chord lines by:

- the first lyric phrase  
- the rhythmic feel  
- the melodic contour  

Showing the first two words:

- anchors the chord line in memory  
- helps with orientation during practice  
- avoids clutter  
- avoids full lyric display  

Two words is a deliberate choice:

- one word is often too vague  
- three words starts to feel like lyrics  

The mode is togglable because some musicians prefer pure chords.

---

# 5. **Why the Input Model Is Immutable**

Once parsed, the data model is never mutated.

This ensures:

- stepping is deterministic  
- backward stepping is safe  
- formatting modes (leading words on/off) do not alter the underlying data  
- future features (transpose, capo, auto‑scroll) can be layered on cleanly  

Immutability is a quiet but important design choice.

---

# 6. **Why the UI Is Three Fixed Regions**

The UI uses:

- `titleDisplay`  
- `sectionDisplay`  
- `display`  

This separation:

- prevents overwriting metadata  
- keeps section headers persistent  
- isolates chord rendering  
- simplifies styling  
- avoids layout shifts  

It also mirrors how musicians mentally structure songs.

---

# 7. **Why There Is No Framework**

Frameworks introduce:

- build steps  
- bundlers  
- dependency management  
- version drift  
- CORS issues  
- deployment complexity  

The tool must be:

- portable  
- hackable  
- inspectable  
- future‑proof  

Plain JS is the right choice.

---

# 8. **Why Keyboard and Tap Are Unified**

The input layer treats:

- tap  
- click  
- Space  
- Enter  
- ArrowRight  

…as the same action.

This is intentional:

- musicians often practise with one hand on the instrument  
- the other hand may be on a trackpad, mouse, or keyboard  
- the tool should adapt to the musician, not the other way around  

Backward stepping is similarly unified.

---

# 9. **Future‑Proofing Considerations**

The architecture is designed to support:

### **9.1 Auto‑transpose**
Because chords are stored as tokens, not raw strings.

### **9.2 Capo‑aware display**
Because the data model is immutable and chords are structured.

### **9.3 Auto‑scroll**
Because tempo and scroll speed are already part of metadata.

### **9.4 Section jump menu**
Because sections are stored in order.

### **9.5 Full lyric mode**
Because lyrics are already captured.

### **9.6 Export to ChordPro**
Because the structure maps cleanly to ChordPro semantics.

---

# 10. **Summary**

ChordReveal’s architecture is shaped by:

- the realities of musicians practising  
- the constraints of running locally in a browser  
- the desire for predictable behaviour  
- the need for clean, maintainable code  
- the avoidance of unnecessary complexity  

Every design choice — from token‑based chord detection to the linear reveal queue — supports these goals.

---

If you want, I can also generate:

- a **system architecture diagram**  
- a **flowchart of the parser**  
- a **sequence diagram for stepping**  
- a **roadmap document** for future features  

Just tell me which one you want next.
