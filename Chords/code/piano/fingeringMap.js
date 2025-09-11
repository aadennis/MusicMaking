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
    C_major: ['C', 'E', 'G'],
    C7: ['C', 'E', 'Asharp']
  };

  const group = document.getElementById(svgGroupId);
  group.innerHTML = ''; // Clear previous dots

  chords[chordName].forEach(note => {
    const pos = getFingeringPosition(note);
    if (pos) {
      const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
      use.setAttributeNS(null, 'href', pos.anchor);
      use.setAttributeNS(null, 'x', pos.x);
      group.appendChild(use);
    }
  });
}