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

  let title = null;
  const sections = [];
  const sectionNames = ["verse", "chorus", "bridge", "intro", "outro"];

  const sectionsWithLines = {};
  let currentSection = null;

  for (const rawLine of lines) {
    const line = rawLine.trim();

    // Title
    const titleMatch = line.match(/\{title:\s*(.+?)\s*\}/i);
    if (titleMatch) title = titleMatch[1];

    // Section markers
    const sectionMatch = line.match(/\{(\w+)\s*:?\s*\}/);
    if (sectionMatch) {
      const sec = sectionMatch[1].toLowerCase();
      if (sectionNames.includes(sec)) {
        const proper = sec.charAt(0).toUpperCase() + sec.slice(1);

        if (!sections.includes(proper)) {
          sections.push(proper);
        }

        currentSection = proper;
        if (!sectionsWithLines[currentSection]) {
          sectionsWithLines[currentSection] = [];
        }
        continue;
      }
    }

    // Chord lines inside a section
    if (currentSection && line.length > 0) {
      const chords = [...line.matchAll(/\[([^\]]+)\]/g)].map(m => m[1].trim());
      if (chords.length > 0) {
        sectionsWithLines[currentSection].push(chords);
      }
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

fileInput.addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  fileInput.style.display = "none";

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

tapArea.addEventListener("click", () => {
  showNext();
});

resetButton.addEventListener("click", () => {
  titleDisplay.textContent = "";
  sectionDisplay.textContent = "";
  display.textContent = "";

  fileInput.value = "";
  fileInput.style.display = "block";

  resetButton.style.display = "none";
});
