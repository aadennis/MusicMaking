const whiteKeyX = {
  'F-2': 0,
  'G-2': 60,
  'A-2': 120,
  'B-2': 180,
  'C-3': 240,
  'D-3': 300,
  'E-3': 360,
  'F-3': 420,
  'G-3': 480,
  'A-3': 540,
  'B-3': 600,
  'C-4': 660
};

const blackKeyX = {
  'F#-2': 40,
  'G#-2': 100,
  'A#-2': 160,
  'C#-3': 280,
  'D#-3': 340,
  'F#-3': 460,
  'G#-3': 520,
  'A#-3': 580,
  'C#-4': 700
};

function getFingeringPosition(note) {
  if (whiteKeyX[note] !== undefined) {
    return { x: whiteKeyX[note] + 30, anchor: '#fingering-anchor' };
  }
  if (blackKeyX[note] !== undefined) {
    return { x: blackKeyX[note] + 20, anchor: '#fingering-anchor-black' };
  }
  return null;
}

function renderFingering(chordName, svgGroupId) {
  const chords = {
    C_major: ['C-3', 'E-3', 'G-3'],
    C7: ['C-3', 'E-3', 'A#-3']
    // Add more chords as needed
  };

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