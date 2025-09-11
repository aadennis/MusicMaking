// White keys: spaced every 60px, starting from F at x=0
const whiteKeyX = {
  F: 0, G: 60, A: 120, B: 180, C: 240, D: 300, E: 360,
  F2: 420, G2: 480, A2: 540, B2: 600, C2: 660
};

// Black keys: 40px wide, centered between white keys, nudged 5px left
const blackKeyX = {
  Fsharp: 40, Gsharp: 100, Asharp: 160,
  Csharp: 280, Dsharp: 340,
  Fsharp2: 460, Gsharp2: 520, Asharp2: 580,
  Csharp2: 700
};

// Fingering dot center = keyX + 30 (half of white key width)
function getFingeringX(note) {
  const x = whiteKeyX[note] ?? blackKeyX[note];
  return x !== undefined ? x + 30 : null;
}

