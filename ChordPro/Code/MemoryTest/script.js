const titleDisplay = document.getElementById("titleDisplay");
const display = document.getElementById("display");
const fileInput = document.getElementById("fileInput");
const resetButton = document.getElementById("resetButton");

function showForSeconds(text, seconds) {
  return new Promise(resolve => {
    display.textContent = text;
    setTimeout(resolve, seconds * 1000);
  });
}

function parseChordPro(text) {
  const lines = text.split(/\r?\n/);

  let title = null;
  const sections = [];
  const sectionNames = ["verse", "chorus", "bridge", "intro", "outro"];

  const sectionsWithChords = {};
  let currentSection = null;

  for (const line of lines) {

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
        if (!sectionsWithChords[currentSection]) {
          sectionsWithChords[currentSection] = [];
        }
        continue;
      }
    }

    // Chords inside a section
    if (currentSection) {
      const chordMatches = [...line.matchAll(/\[([^\]]+)\]/g)];
      for (const m of chordMatches) {
        const chord = m[1].trim();
        if (!sectionsWithChords[currentSection].includes(chord)) {
          sectionsWithChords[currentSection].push(chord);
        }
      }
    }
  }

  return { title, sections, sectionsWithChords };
}

async function runTest(data) {
  if (data.title) {
    titleDisplay.textContent = data.title;
  }

  for (const sec of data.sections) {
    await showForSeconds(sec, 3);
  }

  display.textContent = "";

  // Show reset button after test completes
  resetButton.style.display = "block";

  console.log("Extracted chords:", data.sectionsWithChords);
}

fileInput.addEventListener("change", function() {
  const file = this.files[0];
  if (!file) return;

  // Hide the file input after selection
  fileInput.style.display = "none";

  const reader = new FileReader();
  reader.onload = function(e) {
    const text = e.target.result;
    const data = parseChordPro(text);
    runTest(data);
  };
  reader.readAsText(file);
});

// Reset button logic
resetButton.addEventListener("click", () => {
  // Clear displays
  titleDisplay.textContent = "";
  display.textContent = "";

  // Show file input again
  fileInput.value = "";
  fileInput.style.display = "block";

  // Hide reset button
  resetButton.style.display = "none";
});
