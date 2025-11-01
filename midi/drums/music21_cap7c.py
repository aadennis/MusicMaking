# A — Annotated walkthrough (line-by-line)

# from music21 import *
# Imports the music21 package into the namespace. This makes classes like stream.Stream, chord.Chord, note.Rest available directly.
# import copy
# Imports the Python copy module; used here to deep-copy chord objects so repeated appends are independent objects.
# stream1 = stream.Stream()
# Creates a music21 Stream. A Stream is a container that holds Notes, Chords, Rests, Measures, Parts, etc. This stream will be written out as a single sequence/track when the script writes MIDI.
# chord1 = chord.Chord([38,41]) # kick, snare, tom
# Constructs a Chord whose pitches are specified by MIDI pitch numbers 38 and 41.
# Important correction: MIDI note numbers 36 and 38 are commonly used for kick (36 = Bass Drum 1) and snare (38 = Acoustic Snare). 41 is Low Floor Tom. So the comment "kick, snare, tom" is misleading: chord1 actually contains 38 (snare) and 41 (low floor tom). It does NOT include 36 (kick).
# Each pitch is treated as a pitched MIDI note by music21 unless you specifically mark the part as percussion/unpitched.
# Default duration: a newly created chord has a default quarterLength of 1.0 (a quarter note) unless changed.
# chord2 = chord.Chord([36]) # kick
# A single-pitch chord (effectively a single note) with MIDI pitch 36 (commonly Bass Drum 1 / kick). Also defaults to quarter-note duration.
# stream1.append(copy.deepcopy(chord1))
# Appends a deepcopy of chord1 to the stream. deepcopy is used so each appended chord is an independent object (changes to one won't alter others).
# stream1.append(copy.deepcopy(chord2))
# Appends the kick chord (36) as another quarter-note event following the first.
# stream1.append(copy.deepcopy(chord1))
# Appends chord1 again (snare+tom) — so far the stream has: chord1, chord2, chord1 (three quarter notes).
# r = note.Rest()
# Creates a Rest object. Default duration is a quarter note (quarterLength = 1.0).
# stream1.append(r)
# Appends a quarter-note rest as the fourth event.
# stream1.append(copy.deepcopy(chord1))
# Appends chord1 (snare+tom) as the fifth quarter event.
# stream1.write('midi', fp="c:/temp/x2.mid")
# Writes the Stream to a MIDI file at C:\temp\x2.mid.
# B — High-level summary of the generated MIDI data

# Sequence (in temporal order):
# Quarter note: chord with MIDI pitches 38 and 41 (snare + low tom).
# Quarter note: pitch 36 (kick).
# Quarter note: chord 38 + 41 again.
# Quarter rest.
# Quarter note: chord 38 + 41 again.
# Durations:
# Every element (chords and rest) uses the default quarter-note length (1.0 quarterLength). So total elapsed time = 5 quarter notes (one bar of 4/4 plus one extra quarter, or simply 5 quarter beats in a row).
# MIDI channels / instruments:
# This code never sets an Instrument object or a MIDI channel explicitly. So music21 will use defaults (a pitched instrument / melodic channel). The MIDI note numbers you used correspond to General MIDI percussion notes, but without assigning the part to the percussion channel (MIDI channel 10, zero-based channel index 9) or inserting a percussion instrument, many renderers will treat them as pitched notes.
# Velocities:
# No velocity/dynamic is specified. music21 will emit default MIDI velocities (i.e., medium/default velocity) for each note-on event. The exact numeric value depends on music21's MIDI mapping/version; practically they become medium-intensity hits in a DAW or notation program.
# File written:
# The script creates C:\temp\x2.mid. That file will contain a single track (single stream), with the five quarter-length events described above.
# C — How this will appear in MIDI notation renderers (two common behaviors)

# If the renderer treats the track as pitched (the most likely outcome given the script)
# Staff and clef:
# The notes will appear on a normal pitched staff (treble clef by default unless the renderer chooses otherwise). Since the MIDI pitch numbers are low (36–41), the notes will sit well below middle C — a renderer may show them on the staff in lower ledger lines or switch to bass clef if it auto-adjusts clef for range.
# Visual representation:
# Each chord (38+41) will be drawn as stacked pitched notes (two noteheads vertically aligned) occupying the same rhythmic position (a single quarter-note chord symbol). The single kick (36) will be one notehead (quarter).
# The rest will be a quarter rest.
# Notation layout and measure grouping:
# Because no TimeSignature is set in the stream, many notation programs assume a default (often 4/4). In that case the first four quarter events will fill a 4/4 measure (the first three chords + the rest), and the final quarter note (the fifth) will appear in the next measure alone. Some renderers may place all five quarters in a single measure if they don't enforce a default measure length; but most will break into 4/4 then a 1/4 pickup bar.
# Playback sound:
# The MIDI will produce pitched instrument notes (e.g., piano or GM patch assigned to the track), not necessarily drum kit hits — so the sonic result will likely be pitched tones at low pitch (likely very bass-y piano or whatever default program is used).
# Summary: visually it looks like a low-pitched chord rhythm (quarter, quarter, quarter, rest, quarter), stacked noteheads for chords, not as standard drum notation.
# If the renderer recognizes or is instructed to treat the track as percussion/drumset
# Drum staff and notation:
# In drum notation, each percussion item maps to a specific staff line/position and a specific unpitched notehead (often an X or small notehead depending on instrument). A drum clef or single-line percussion staff may be used.
# Standard GM mapping: 36 = Bass Drum (notated typically on the lowest line/space), 38 = Acoustic Snare (notated on the snare line), 41 = Low Floor Tom (tom line). If the renderer receives MIDI channel 10 (percussion channel) or the part is a drumset/percussion instrument, it will map the MIDI note numbers to percussion notation.
# Visual representation in percussion mode:
# The kick (36) will appear as a kick drum symbol on the kick line. The chord [38,41] will be rendered as simultaneous snare + low tom hits — on a single percussion staff these will show as two hits at the same beat (stacked vertically but using percussion noteheads or staff positions appropriate for drumset notation). They are not shown as pitched stacked noteheads; instead they appear as unpitched hits on their assigned lines/spaces.
# Measure grouping and timing:
# Just like in pitched mode, the quarter durations will be shown as quarter-note percussion hits; measure grouping follows the time signature rules (if none set, many renderers default to 4/4).
# Playback:
# If the renderer/DAW uses percussion channel mapping then the sounds will be actual drum/kit samples (bass drum, snare, tom) rather than pitched instrument tones.
# How to get this behavior from the current code:
# You must mark the part/stream as percussion or put an Instrument that music notation/MIDI writers recognize as Unpitched/Percussion. Two common approaches:
# Insert a percussion instrument into the stream (example: insert an instance of a percussion/drumset Instrument object if available in your music21 version).
# Or set the MIDI channel for the Part/Stream to channel 9 (MIDI channel 10 in 1-based numbering). Many notation programs detect channel 10 and display percussion notation.
# Example (pseudo-code, check music21 docs for exact API):
# part.insert(0, instrument.Percussion() ) # or instrument.DrumKit() / instrument.UnpitchedPercussion()
# or set part.activeSite.midiChannel = 9 (or the relevant attribute) before writing MIDI.
# Without these changes, most notation renderers will treat the notes as pitched.
# D — Small corrections, suggestions, and edge cases

# Fix the comment: change the comment on chord1 to reflect the actual notes you used (e.g., "# snare (38), low tom (41)").
# If you intended chord1 to be kick+snare+tom, use [36,38,41].
# If you want percussion notation in notation software:
# Insert a percussion instrument into the stream (per music21 docs), or set the MIDI channel to 10 (channel index 9).
# If you want more realistic drum playback (per-instrument velocities), set Note.velocity or dynamics prior to writing.
# Duration/measure control:
# If you want the five quarters to stay inside a single 5/4 measure, insert a TimeSignature('5/4') at the start of the stream.
# If you want a standard 4/4 bar then the current output will naturally group into a 4/4 followed by a 1/4 bar.
# Visual stacking in pitched mode:
# Stacked chords will show as pitched intervals — which may look odd for drum kit numbers (because drums are not pitched in standard notation), so ensure you pick the percussion path if you want conventional drum notation.
# If you want per-hit dynamics/velocity:
# Create explicit Note/Chord objects and set .volume.velocity (or use dynamics objects) before writing.
# E — Short examples (what to change to get percussion notation)

# Minimal change idea (conceptual — verify API on your music21 version):
# Insert a percussion instrument at the start of the stream, e.g.:
# stream1.insert(0, instrument.Percussion()) # or instrument.DrumKit()
# Or create a Part, set its midiChannel to 9 (percussion channel), append the chords to that part, then put part into a Score and write MIDI/XML.
# To control time signature so notation groups predictably:
# from music21 import meter
# stream1.insert(0, meter.TimeSignature('4/4')) # makes the first four quarter notes a measure
# F — Quick checklist of what the script currently does vs. what you might want

# Currently:
# Outputs a single-track MIDI with 5 quarter-length items: [chord(38,41), chord(36), chord(38,41), rest, chord(38,41)].
# No instrument/percussion designation — so notation renderers will usually show pitched notation.
# If you want:
# Drum notation & correct drum sounds -> designate the part as percussion/drum channel.
# Accurate comments/intent -> correct the comment and/or add explicit pitch 36 to chord1 if desired.
# Specific dynamics or articulations -> set velocities or add dynamic marks.
# G — Final notes about common renderer behavior

# Many DAWs will play back the MIDI irrespective of channel as note numbers; if the MIDI channel is not 10, the DAW will choose whatever instrument/patch is assigned to that track — so you may hear piano instead of drum kit.
# Notation programs like MuseScore, Finale, Sibelius will show drum notation only if the track is recognized as percussion (instrument set as drum kit or on percussion channel). If not, they will use pitched staves and show ledger lines for low pitches.
# If you want me to, I can:
# Edit the script to set instrument to a drum/percussion instrument and demonstrate a corrected example.
# Create an updated version that writes MusicXML instead of MIDI so notation is clearer to inspect in a combined view (MusicXML preserves instrument and staff information better for notation programs).
# Progress update



from music21 import *
import copy

stream1 = stream.Stream()
chord1 = chord.Chord([38,41]) # kick, snare, tom
chord2 = chord.Chord([36])   # kick

stream1.append(copy.deepcopy(chord1))

stream1.append(copy.deepcopy(chord2))

stream1.append(copy.deepcopy(chord1))

r = note.Rest()
stream1.append(r)
stream1.append(copy.deepcopy(chord1))

stream1.write('midi', fp="c:/temp/x2.mid")