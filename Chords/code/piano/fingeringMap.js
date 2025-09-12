const whiteKeyX = {
  'F-2': 0,
  'G-2': 42,
  'A-2': 84,
  'B-2': 126,
  'C-3': 168,
  'D-3': 210,
  'E-3': 252,
  'F-3': 294,
  'G-3': 336,
  'A-3': 378,
  'B-3': 420,
  'C-4': 462,
};

const blackKeyX = {
  'F#-2': 28,
  'G#-2': 70,
  'A#-2': 112,
  'C#-3': 196,
  'D#-3': 238,
  'F#-3': 322,
  'G#-3': 364,
  'A#-3': 406,
  'C#-4': 490,
};

const WHITE_KEY_WIDTH = 42;
const BLACK_KEY_WIDTH = 28;

function getFingeringPosition(note) {
  if (whiteKeyX[note] !== undefined) {
    return { x: whiteKeyX[note] + WHITE_KEY_WIDTH / 2, anchor: '#fingering-anchor' };
  }
  if (blackKeyX[note] !== undefined) {
    return { x: blackKeyX[note] + BLACK_KEY_WIDTH / 2, anchor: '#fingering-anchor-black' };
  }
  return null;
}

function renderFingering(chordName, svgGroupId) {

  const group = document.getElementById(svgGroupId);
  group.innerHTML = ''; // Clear previous dots

  const notes = chords[chordName];
  notes.forEach(note => {
    const pos = getFingeringPosition(note);
    if (pos) {
      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttributeNS(null, 'href', pos.anchor);
      use.setAttributeNS(null, 'x', pos.x);
      group.appendChild(use);
    }
  });

  // Update caption with chord name and notes
  const caption = document.getElementById('chord-caption');
  caption.textContent = `${chordName}: ${notes.join(', ')}`;
}