(() => {
  const mount = document.getElementById("app") || document.body;
  const defaultTitle = document.title || "Chord Sheet";

  // --- Build UI in JS ---
  const statusEl = el("span", { className: "status", id: "status" }, [
    "Drop a .md file below (or click to pick).",
  ]);

  const clearBtn = el(
    "button",
    { className: "btn", id: "clearBtn", type: "button", disabled: true },
    ["Clear"]
  );

  const top = el("div", { className: "top" }, [
    el("strong", {}, ["Chord Sheet Viewer"]),
    el("div", { className: "actions" }, [clearBtn, statusEl]),
  ]);

  const filePicker = el("input", {
    id: "filePicker",
    type: "file",
    accept: ".md,.markdown,.txt,text/markdown,text/plain",
    hidden: true,
  });

  const dropzone = el(
    "div",
    {
      id: "dropzone",
      className: "dropzone",
      tabIndex: 0,
      role: "button",
      ariaLabel: "Drop markdown file here",
    },
    [
      el("div", {}, [el("strong", {}, ["Drag & drop"]), " a Markdown file here"]),
      el("div", { className: "hint" }, [
        "Or ",
        el("u", {}, ["click"]),
        " this box to choose a file.",
      ]),
      filePicker,
    ]
  );

  const content = el("div", { id: "content", className: "content" }, [
    "Nothing loaded yet.",
  ]);

  mount.append(top, dropzone, content);

  const setStatus = (msg) => (statusEl.textContent = msg);

  function setTitleForFile(fileName) {
    document.title = fileName ? `${fileName} — ${defaultTitle}` : defaultTitle;
  }

  function renderMarkdown(text) {
    content.innerHTML = marked.parse(text);
  }

  function readFileAsText(file) {
    // FileReader reads files provided via input selection or drag & drop. [4](https://www.npmjs.com/package/marked)
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result || "");
      reader.onerror = () => reject(reader.error || new Error("Failed to read file"));
      reader.readAsText(file);
    });
  }

  async function handleFile(file) {
    if (!file) return;

    const name = file.name || "unnamed file";
    setStatus(`Loading: ${name}`);

    try {
      const text = await readFileAsText(file);
      renderMarkdown(text);
      setStatus(`Rendered: ${name}`);
      setTitleForFile(name);
      clearBtn.disabled = false;
    } catch (err) {
      console.error(err);
      content.textContent = String(err.message || err);
      setStatus(`Error reading: ${name}`);
      // keep Clear disabled if nothing successfully rendered
    }
  }

  function clearView() {
    // Reset UI state
    content.textContent = "Nothing loaded yet.";
    setStatus("Drop a .md file below (or click to pick).");
    setTitleForFile("");
    clearBtn.disabled = true;
    filePicker.value = "";
    dropzone.focus();
  }

  clearBtn.addEventListener("click", clearView);

  // --- Drag & Drop events ---
  ["dragenter", "dragover", "dragleave", "drop"].forEach((evt) => {
    dropzone.addEventListener(evt, (e) => {
      e.preventDefault();
      e.stopPropagation();
    });
  });

  dropzone.addEventListener("dragenter", () => dropzone.classList.add("dragover"));
  dropzone.addEventListener("dragover", () => dropzone.classList.add("dragover"));
  dropzone.addEventListener("dragleave", () => dropzone.classList.remove("dragover"));

  dropzone.addEventListener("drop", async (e) => {
    dropzone.classList.remove("dragover");

    // Dropped local files arrive via DragEvent.dataTransfer.files. [3](https://paulserban.eu/blog/post/how-to-debug-blocked-requests-local-network-access-in-chrome/)[4](https://www.npmjs.com/package/marked)
    const files = e.dataTransfer && e.dataTransfer.files;
    if (files && files.length) {
      await handleFile(files[0]);
    } else {
      setStatus("No file detected in drop.");
    }
  });

  // --- Click-to-pick fallback ---
  dropzone.addEventListener("click", () => filePicker.click());
  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      filePicker.click();
    }
  });

  filePicker.addEventListener("change", async () => {
    const file = filePicker.files && filePicker.files[0];
    await handleFile(file);
    // allow selecting same file again later
    filePicker.value = "";
  });

  // Prevent navigation if dropping outside the dropzone
  window.addEventListener("dragover", (e) => e.preventDefault());
  window.addEventListener("drop", (e) => e.preventDefault());

  // --- helper to create DOM nodes ---
  function el(tag, props = {}, children = []) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(props)) {
      if (k === "ariaLabel") node.setAttribute("aria-label", v);
      else if (k in node) node[k] = v;
      else node.setAttribute(k, v);
    }
    for (const child of children) {
      node.append(child instanceof Node ? child : document.createTextNode(String(child)));
    }
    return node;
  }
})();
