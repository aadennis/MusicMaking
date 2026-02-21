// --- DOM ELEMENTS ---
const titleDisplay = document.getElementById("titleDisplay");
const sectionDisplay = document.getElementById("sectionDisplay");
const display = document.getElementById("display");
const fileInput = document.getElementById("fileInput");
const resetButton = document.getElementById("resetButton");
const tapArea = document.getElementById("tapArea");

// --- REVEAL ENGINE STATE ---
let revealQueue = [];   // Flattened list of items to reveal
let revealIndex = 0;    // Pointer into revealQueue
let leadingWordsMode = true; // Toggle for lyric-prefix mode

// ------------------------------------------------------------
// PARSER
// Reads metadata, sections, chord lines, and lyric lines.
// Produces: { meta, sections, sectionsWithLines }
// ------------------------------------------------------------
function parseChordPro(text) {
  const lines = text.split(/\r?\n/);

  // --- METADATA ---
  const meta = {};
  let inMetadata = true;

  // --- SONG STRUCTURE ---
  const sections = [];
  const sectionsWithLines = {};
  let currentSection = null;
  let skipSection = false;

  // --- CHORD DETECTION ---
  function isChordToken(tok) {
    return /^[A-G][#b]?(m|M|maj|min|dim|aug|sus|add)?\d*$/.test(tok);
  }

  function isChordLine(rawLine) {
    // Remove leading indentation only
    const trimmed = rawLine.replace(/^\s+/, "");
    if (trimmed.length === 0) return false;

    const tokens = trimmed.split(/\s+/);
    if (tokens.length === 0) return false;

    return tokens.every(isChordToken);
  }

  // --- MAIN LOOP ---
  for (const rawLine of lines) {
    const line = rawLine.trim();

    // --- METADATA BLOCK ---
    if (inMetadata) {
      if (line.startsWith("#")) {
        const [tag, ...rest] = line.slice(1).split(":");
        meta[tag.trim()] = rest.join(":").trim();
        continue;
      }

      if (line.length === 0) continue; // allow blank line after metadata

      inMetadata = false; // first real line ends metadata block
    }

    // --- SECTION HEADER ---
    if (line.startsWith("[") && line.endsWith("]")) {
      currentSection = line.slice(1, -1).trim();

      // Skip Solo sections entirely
      skipSection = currentSection.toLowerCase() === "solo";

      if (!skipSection) {
        sections.push(currentSection);
        sectionsWithLines[currentSection] = [];
      }

      continue;
    }

    if (skipSection) continue;

    // --- CHORD LINE ---
    if (currentSection && isChordLine(rawLine)) {
      const trimmed = rawLine.replace(/^\s+/, "");
      const chords = trimmed.split(/\s+/).filter(Boolean);

      // Store chord line with lyric placeholder
      sectionsWithLines[currentSection].push({
        chords,
        lyric: null
      });

      continue;
    }

    // --- LYRIC LINE ---
    if (currentSection && line.length > 0) {
      const last = sectionsWithLines[currentSection][sectionsWithLines[currentSection].length - 1];
      if (last && last.lyric === null) {
        last.lyric = line; // associate lyric with previous chord line
      }
      continue;
    }
  }

  return { meta, sections, sectionsWithLines };
}

// ------------------------------------------------------------
// FORMATTER
// Produces the final display string for a chord line.
// ------------------------------------------------------------
function formatLine(entry) {
  if (!leadingWordsMode || !entry.lyric) {
    return entry.chords.join("   ");
  }

  const words = entry.lyric.split(/\s+/).slice(0, 2).join(" ");
  return `${words} : ${entry.chords.join("   ")}`;
}

// ------------------------------------------------------------
// REVEAL QUEUE BUILDER
// Converts structured data into a linear reveal sequence.
// ------------------------------------------------------------
function prepareRevealQueue(data) {
  revealQueue = [];

  for (const sec of data.sections) {
    revealQueue.push({ type: "section", name: sec });

    for (const entry of data.sectionsWithLines[sec]) {
      revealQueue.push({ type: "line", entry });
    }

    revealQueue.push({ type: "blank" });
  }

  revealIndex = 0;
}

// ------------------------------------------------------------
// RENDERING FUNCTIONS
// ------------------------------------------------------------
function showNext() {
  if (revealIndex >= revealQueue.length) {
    display.textContent = "";
    return;
  }

  const item = revealQueue[revealIndex];
  revealIndex++;

  if (item.type === "section") {
    sectionDisplay.textContent = item.name;
    display.textContent = "";
    return;
  }

  if (item.type === "line") {
    display.textContent = formatLine(item.entry);
    return;
  }

  if (item.type === "blank") {
    display.textContent = "";
    return;
  }
}

function showPrevious() {
  revealIndex = Math.max(0, revealIndex - 1);
  const item = revealQueue[revealIndex];

  if (item.type === "section") {
    sectionDisplay.textContent = item.name;
    display.textContent = "";
    return;
  }

  if (item.type === "line") {
    display.textContent = formatLine(item.entry);
    return;
  }

  if (item.type === "blank") {
    display.textContent = "";
    return;
  }
}

// ------------------------------------------------------------
// METADATA DISPLAY
// ------------------------------------------------------------
function displayMetadata(meta) {
  titleDisplay.innerHTML = "";

  if (meta.title) {
    const t = document.createElement("div");
    t.className = "songTitle";
    t.textContent = meta.title;
    titleDisplay.appendChild(t);
  }

  if (meta.artist) {
    const a = document.createElement("div");
    a.className = "songArtist";
    a.textContent = meta.artist;
    titleDisplay.appendChild(a);
  }
}

// ------------------------------------------------------------
// FILE LOADING
// ------------------------------------------------------------
tapArea.classList.add("disabled");

fileInput.addEventListener("change", function () {
  const file = this.files[0];
  if (!file) return;

  fileInput.style.display = "none";
  tapArea.classList.remove("disabled");

  const reader = new FileReader();
  reader.onload = function (e) {
    const text = e.target.result;
    const data = parseChordPro(text);

    if (data.meta) displayMetadata(data.meta);

    prepareRevealQueue(data);
    showNext();
  };
  reader.readAsText(file);
});

// ------------------------------------------------------------
// INPUT HANDLERS
// ------------------------------------------------------------
tapArea.addEventListener("click", showNext);

document.addEventListener("keydown", (e) => {
  if (["Space", "Enter", "ArrowRight"].includes(e.code)) {
    e.preventDefault();
    showNext();
  }

  if (["ArrowLeft", "Backspace"].includes(e.code)) {
    e.preventDefault();
    showPrevious();
  }

  if (e.code === "KeyL") {
    leadingWordsMode = !leadingWordsMode;
  }
});
