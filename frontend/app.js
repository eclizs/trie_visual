// ---- Mode switching ----
const modeBtns = document.querySelectorAll(".mode-btn");
const panels = {
  search: document.getElementById("panel-search"),
  add: document.getElementById("panel-add"),
  delete: document.getElementById("panel-delete"),
};

modeBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    modeBtns.forEach((b) => {
      b.classList.remove("is-active");
      b.setAttribute("aria-selected", "false");
    });
    btn.classList.add("is-active");
    btn.setAttribute("aria-selected", "true");

    Object.values(panels).forEach((p) => p.classList.remove("is-active"));
    panels[btn.dataset.mode].classList.add("is-active");
  });
});

// ---- Search ----
const searchInput = document.getElementById("search-input");
const resultsList = document.getElementById("results-list");
const searchBox = document.querySelector(".search-box");
let debounceTimer;
let highlightedIndex = -1;
let count;

searchInput.addEventListener("input", () => {
  clearTimeout(debounceTimer);
  let prefix = searchInput.value.trim();
  count = prefix.slice(0, prefix.indexOf(" "))
  prefix = prefix.slice(prefix.indexOf(" ")+1)
  debounceTimer = setTimeout(() => runSearch(prefix), 200);
});

searchInput.addEventListener("keydown", (e) => {
  const items = resultsList.querySelectorAll(".entry-item:not(.is-empty)");
  if (!resultsList.classList.contains("is-open") || items.length === 0) return;

  if (e.key === "ArrowDown" || (e.key === "Tab" && !e.shiftKey)) {
    e.preventDefault();
    highlightedIndex = Math.min(highlightedIndex + 1, items.length - 1);
    updateHighlight(items);
  } else if (e.key === "ArrowUp" || (e.key === "Tab" && e.shiftKey)) {
    e.preventDefault();
    highlightedIndex = Math.max(highlightedIndex - 1, 0);
    updateHighlight(items);
  } else if (e.key === "Enter") {
    if (highlightedIndex >= 0 && items[highlightedIndex]) {
      e.preventDefault();
      selectWord(count + " " + items[highlightedIndex].dataset.word);
    }
  } else if (e.key === "Escape") {
    closeDropdown();
  }
});

document.addEventListener("click", (e) => {
  if (!searchBox.contains(e.target)) closeDropdown();
});

function updateHighlight(items) {
  items.forEach((item, i) => {
    item.classList.toggle("is-highlighted", i === highlightedIndex);
  });
  if (items[highlightedIndex]) {
    items[highlightedIndex].scrollIntoView({ block: "nearest" });
  }
}

const savedList = document.getElementById("saved-list");
const savedWords = [];

function selectWord(word) {
  savedWords.push(word);
  renderSavedWords();
  // searchInput.value = "";
  closeDropdown();
  // resultsList.innerHTML = "";
  searchInput.focus();
}

function renderSavedWords() {
  savedList.textContent = savedWords.length ? savedWords.join("\n") : "(none yet)";
}

function openDropdown() {
  resultsList.classList.add("is-open");
  searchInput.setAttribute("aria-expanded", "true");
}

function closeDropdown() {
  resultsList.classList.remove("is-open");
  searchInput.setAttribute("aria-expanded", "false");
  highlightedIndex = -1;
}

async function runSearch(prefix) {
  if (!prefix) {
    prefix = ""
  }

  try {
    const res = await fetch(`/search?prefix=${encodeURIComponent(prefix)}`);
    if (!res.ok) throw new Error(`Search failed (${res.status})`);
    const data = await res.json();
    renderResults(data.words || []);
  } catch (err) {
    renderMessage("Error: Unprocessable content");
  }
}

function renderMessage(message) {
  highlightedIndex = -1;
  resultsList.innerHTML = `<li class="entry-item is-empty">${escapeHtml(message)}</li>`;
  openDropdown();
}

function renderResults(words) {
  if (words.length === 0) {
    renderMessage("No matches found.");
    return;
  }

  highlightedIndex = -1;
  resultsList.innerHTML = words
    .map((w) => {
      const path = w.toLowerCase().split("").join(" → ");
      return `<li class="entry-item" data-word="${escapeHtml(w)}" role="option">
        <div class="entry-word">${escapeHtml(w)}</div>
        <div class="entry-path">${escapeHtml(path)}</div>
      </li>`;
    })
    .join("");

  resultsList.querySelectorAll(".entry-item").forEach((item) => {
    item.addEventListener("click", () => selectWord(count + " " + item.dataset.word));
  });

  openDropdown();
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ---- Add ----
const addInput = document.getElementById("add-input");
const addBtn = document.getElementById("add-btn");
const addStatus = document.getElementById("add-status");

addBtn.addEventListener("click", async () => {
  const word = addInput.value.trim();
  if (!word) {
    setStatus(addStatus, "Type a word first.", "err");
    return;
  }

  try {
    const res = await fetch(`/insert?word=${encodeURIComponent(word)}`, {
      method: "POST",
    });
    const data = await res.json().catch(() => ({}));

    if (res.ok) {
      setStatus(addStatus, data.message || `Added "${word}".`, "ok");
      addInput.value = "";
    } else {
      setStatus(addStatus, data.detail || `Could not add "${word}".`, "err");
    }
  } catch (err) {
    setStatus(addStatus, "Error: Unprocessable content", "err");
  }
});

// ---- Delete ----
const deleteInput = document.getElementById("delete-input");
const deleteBtn = document.getElementById("delete-btn");
const deleteStatus = document.getElementById("delete-status");

deleteBtn.addEventListener("click", async () => {
  const word = deleteInput.value.trim();
  if (!word) {
    setStatus(deleteStatus, "Type a word first.", "err");
    return;
  }

  try {
    const res = await fetch(`/delete?word=${encodeURIComponent(word)}`, {
      method: "DELETE",
    });
    const data = await res.json().catch(() => ({}));

    if (res.ok) {
      setStatus(deleteStatus, data.message || `Deleted "${word}".`, "ok");
      deleteInput.value = "";
    } else {
      setStatus(deleteStatus, data.detail || `Could not delete "${word}".`, "err");
    }
  } catch (err) {
    setStatus(deleteStatus, "Error: Unprocessable content", "err");
  }
});

function setStatus(el, message, kind) {
  el.textContent = message;
  el.className = `status-msg ${kind}`;
}