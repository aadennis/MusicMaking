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
  let meta = {};
  let inMetadata = true;
  const lines = text.split(/\r?\n/);

  const sections = [];
  const sectionsWithLines = {};

  let currentSection = null;
  let skipSection = false;

  function isChordToken(token) {
    // Accepts: Em, A7, Bbaug, G#dim, F#m7, Cadd9, %, |
    if (token === "|" || token === "%") return true;
    return /^[A-G][#b]?(m|M|maj|min|dim|aug|sus|add)?\d*$/.test(token);
  }

  function isChordLine(rawLine) {
    const trimmed = rawLine.replace(/^\s+/, "");  // remove leading spaces only
    if (trimmed.length === 0) return false;

    const tokens = trimmed.split(/\s+/);
    return tokens.length > 0 && tokens.every(isChordToken);
  }

  for (const rawLine of lines) {
    const line = rawLine.trim();

    // METADATA BLOCK
    if (inMetadata) {
        if (line.startsWith("#")) {
        const [tag, ...rest] = line.slice(1).split(":");
        meta[tag.trim()] = rest.join(":").trim();
        continue;
        }

        // First non-metadata line ends the metadata block
        if (line.length === 0) continue; // allow blank line after metadata
        inMetadata = false;
    }


    // SECTION HEADER
    if (line.startsWith("[") && line.endsWith("]")) {
      currentSection = line.slice(1, -1);

      // NEW RULE: skip Solo entirely
      skipSection = currentSection.toLowerCase() === "solo";

      if (!skipSection) {
        sections.push(currentSection);
        sectionsWithLines[currentSection] = [];
      }

      continue;
    }

    // If skipping (Solo), ignore everything
    if (skipSection) continue;

    // CHORD LINE
    if (currentSection && isChordLine(rawLine)) {

        console.log("CHORD LINE:", rawLine);   // ← correct place

        const chords = rawLine
        .trim()
        .split(/\s+/)
        .filter(x => x.length > 0);

        sectionsWithLines[currentSection].push(chords);
        continue;
}

  }

  return { meta, sections, sectionsWithLines };
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

document.addEventListener("click", (e) => {
  // Ignore clicks on buttons or file input
  if (e.target === fileInput || e.target === resetButton) return;

  console.log("WINDOW CLICK");
  showNext();
});

