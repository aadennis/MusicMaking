const titleDisplay = document.getElementById("titleDisplay");
const sectionDisplay = document.getElementById("sectionDisplay");
const display = document.getElementById("display");
const fileInput = document.getElementById("fileInput");
const resetButton = document.getElementById("resetButton");
const tapArea = document.getElementById("tapArea");

let revealQueue = [];
let revealIndex = 0;
let waitingForTap = false;
let leadingWordsMode = true;

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
    // Remove leading spaces only (indentation allowed)
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

      // First non-metadata line ends metadata block
      inMetadata = false;
    }

    // --- SECTION HEADER ---
    if (line.startsWith("[") && line.endsWith("]")) {
      currentSection = line.slice(1, -1).trim();

      skipSection = currentSection.toLowerCase() === "solo";

      if (!skipSection) {
        sections.push(currentSection);
        sectionsWithLines[currentSection] = [];
      }

      continue;
    }

    // Skip Solo section entirely
    if (skipSection) continue;

    // --- CHORD LINE DETECTION ---
    if (currentSection && isChordLine(rawLine)) {
      const trimmed = rawLine.replace(/^\s+/, "");
      const chords = trimmed.split(/\s+/).filter(Boolean);

      sectionsWithLines[currentSection].push({
        chords,
        lyric: null
      });

      continue;
    }

// --- LYRICS ---
if (currentSection && !isChordLine(rawLine) && line.length > 0) {
  const last = sectionsWithLines[currentSection][sectionsWithLines[currentSection].length - 1];
  if (last && last.lyric === null) {
    last.lyric = line;   // store the lyric line
  }
  continue;
}
  }

  return { meta, sections, sectionsWithLines };
}

function prepareRevealQueue(data) {
  revealQueue = [];

  for (const sec of data.sections) {
    revealQueue.push({ type: "section", name: sec });
    for (const entry of data.sectionsWithLines[sec]) {
      revealQueue.push({ type: "line", entry });
    }
    revealQueue.push({ type: "blank" }); // blank between sections
  }

  revealIndex = 0;
}

function showNext() {
  if (revealIndex >= revealQueue.length) {
    display.textContent = ""; // nothing left
    return;
  }

  const item = revealQueue[revealIndex];
  revealIndex++;

  if (item.type === "section") {
    sectionDisplay.textContent = item.name;
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
  // Step back one item
  revealIndex = Math.max(0, revealIndex - 1);

  const item = revealQueue[revealIndex];

  if (item.type === "section") {
    sectionDisplay.textContent = item.name;
    display.textContent = "";
    return;
  }

  if (item.type === "line") {
    display.textContent = item.chords.join("   ");
    return;
  }

  if (item.type === "blank") {
    display.textContent = "";
    return;
  }
}

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

  const info = [];

//   if (meta["key-original"]) info.push(`Orig: ${meta["key-original"]}`);
//   if (meta["key-me"]) info.push(`You: ${meta["key-me"]}`);
//   if (meta.capo) info.push(`Capo: ${meta.capo}`);
//   if (meta.tempo) info.push(`Tempo: ${meta.tempo}`);
//   if (meta.scroll_speed) info.push(`Scroll: ${meta.scroll_speed}`);

  if (info.length > 0) {
    const m = document.createElement("div");
    m.className = "songMeta";
    m.textContent = info.join("   ");
    titleDisplay.appendChild(m);
  }
}

function formatLine(item) {
  if (!leadingWordsMode) {
    return item.chords.join("   ");
  }

  if (!item.lyric) {
    return item.chords.join("   ");
  }

  const words = item.lyric.split(/\s+/).slice(0, 2).join(" ");
  return `${words} : ${item.chords.join("   ")}`;
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
    if (data.meta) {
        displayMetadata(data.meta)
    }
    
    prepareRevealQueue(data);
    console.log("REVEAL QUEUE:", revealQueue);

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

tapArea.addEventListener("click", () => {
  console.log("TAP!");
  showNext();
});

document.addEventListener("keydown", (e) => {
  if (e.code === "Space" || e.code === "Enter" || e.code === "ArrowRight") {
    e.preventDefault();   // stops spacebar from scrolling
    console.log("KEY TAP:", e.code);
    showNext();
  }
});

document.addEventListener("keydown", (e) => {
  if (e.code === "ArrowLeft" || e.code === "Backspace") {
    e.preventDefault();
    console.log("KEY BACK:", e.code);
    showPrevious();
  }
});

