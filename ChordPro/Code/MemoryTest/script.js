const titleDisplay = document.getElementById("titleDisplay");
const sectionDisplay = document.getElementById("sectionDisplay");
const display = document.getElementById("display");
const fileInput = document.getElementById("fileInput");
const resetButton = document.getElementById("resetButton");
const tapArea = document.getElementById("tapArea");

let revealQueue = [];
let revealIndex = 0;
let waitingForTap = false;

function parseChordPro(text) {
  const lines = text.split(/\r?\n/);

  let title = null; // JSON will fill this later
  const sections = [];
  const sectionsWithLines = {};

  let currentSection = null;
  let expectChordLine = false;
  let skipSection = false; // NEW RULE

  // A chord token in your format: Em, A7, Bbaug, G#dim, %, |
  function isChordToken(token) {
    return (
      token === "|" ||
      token === "%" ||
      /^[A-G][#b]?(m|M|maj|min|dim|aug|sus|add)?\d*$/.test(token)
    );
  }

  function isChordLine(rawLine) {
    const tokens = rawLine.trim().split(/\s+/);
    if (tokens.length === 0) return false;
    return tokens.every(t => isChordToken(t));
  }

  for (const rawLine of lines) {
    const line = rawLine.trim();

    // SECTION HEADER: [Verse 1], [Chorus], [Solo], etc.
    const sectionMatch = line.match(/^\[(.+?)\]$/);
    if (sectionMatch) {
      currentSection = sectionMatch[1];

      // NEW RULE: skip Solo section entirely
      skipSection = currentSection.toLowerCase() === "solo";

      if (!skipSection) {
        sections.push(currentSection);
        sectionsWithLines[currentSection] = [];
        expectChordLine = true;
      }

      continue;
    }

    // If we're in a skipped section, ignore everything
    if (skipSection) continue;

    // CHORD LINE
    if (currentSection && expectChordLine && isChordLine(rawLine)) {
      const chords = rawLine
        .trim()
        .split(/\s+/)
        .filter(x => x.length > 0);

      sectionsWithLines[currentSection].push(chords);
      expectChordLine = false; // next line is lyrics
      continue;
    }

    // LYRIC LINE (ignored)
    if (currentSection && !expectChordLine) {
      expectChordLine = true; // next line should be chord line
      continue;
    }
  }

  return { title, sections, sectionsWithLines };
}

function prepareRevealQueue(data) {
  revealQueue = [];

  for (const sec of data.sections) {
    revealQueue.push({ type: "section", name: sec });
    for (const chordLine of data.sectionsWithLines[sec]) {
      revealQueue.push({ type: "line", chords: chordLine });
    }
    revealQueue.push({ type: "blank" }); // blank between sections
  }

  revealIndex = 0;
}

function showNext() {
  if (revealIndex >= revealQueue.length) return;

  const item = revealQueue[revealIndex];
  revealIndex++;

  display.innerHTML = "";
  sectionDisplay.textContent = "";

  if (item.type === "section") {
    sectionDisplay.textContent = item.name;
  }

  if (item.type === "line") {
    const div = document.createElement("div");
    div.className = "lineBox";
    div.textContent = item.chords.join("   ");
    display.appendChild(div);
  }

  if (item.type === "blank") {
    display.textContent = "";
  }
}

// INITIAL STATE
tapArea.classList.add("disabled");

fileInput.addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  // Hide file input
  fileInput.style.display = "none";

  // ENABLE TAP AREA NOW THAT A FILE IS LOADED
  tapArea.classList.remove("disabled");

  const reader = new FileReader();
  reader.onload = function (e) {
    const text = e.target.result;
    const data = parseChordPro(text);

    titleDisplay.textContent = data.title;

    prepareRevealQueue(data);
    showNext();
  };
  reader.readAsText(file);
});

resetButton.addEventListener("click", () => {
  titleDisplay.textContent = "";
  sectionDisplay.textContent = "";
  display.textContent = "";

  fileInput.value = "";
  fileInput.style.display = "block";

  resetButton.style.display = "none";

  // DISABLE TAP AREA AGAIN
  tapArea.classList.add("disabled");
});
