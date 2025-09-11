const whiteKeyX = {
  F: 0, G: 60, A: 120, B: 180, C: 240, D: 300, E: 360,
  F2: 420, G2: 480, A2: 540, B2: 600, C2: 660
};

const blackKeyX = {
  Fsharp: 40, Gsharp: 100, Asharp: 160,
  Csharp: 280, Dsharp: 340,
  Fsharp2: 460, Gsharp2: 520, Asharp2: 580,
  Csharp2: 700
};

function getFingeringX(note) {
  if (whiteKeyX[note] !== undefined) {
    return whiteKeyX[note] + 30; // center of 60px white key
  }
  if (blackKeyX[note] !== undefined) {
    return blackKeyX[note] + 20; // center of 40px black key
  }
  return null;
}

function renderFingering(chordName, svgGroupId) {
  const chords = {
    C_major: ['C', 'E', 'G'],
    C7: ['C', 'E', 'Asharp']
  };

  const group = document.getElementById(svgGroupId);
  group.innerHTML = ''; // Clear previous dots

  chords[chordName].forEach(note => {
    const x = getFingeringX(note);
    if (x !== null) {
      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttributeNS(null, 'href', '#fingering-anchor');
      use.setAttributeNS(null, 'x', x);
      group.appendChild(use);
    }
  });
}