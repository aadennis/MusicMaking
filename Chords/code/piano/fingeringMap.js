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
  'D-4': 702,
  'E-4': 744,
  'F-4': 786,
  'G-4': 828,
  'A-4': 870,
  'B-4': 912,
  'C-5': 954,
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
  'D#-4': 726,  // between D-4 (702) and E-4 (744)
  'F#-4': 810,  // between F-4 (786) and G-4 (828)
  'G#-4': 852,  // between G-4 (828) and A-4 (870)
  'A#-4': 894,  // between A-4 (870) and B-4 (912)
  'C#-5': 936,  // between B-4 (912) and C-5 (954)

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