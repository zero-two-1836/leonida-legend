// Leonida Legend — boot and wiring.
//
// Loads the trophy data (a file of this app, fetched relatively, so the
// guide works from any static server with the network off), builds the
// tracker, and connects the controls: search, grade and kind filters, the
// spoiler shield, progress export/import/reset, and the four views
// (Tracker, Roadmap, Missables, Sources).
//
// The views can also be addressed by URL — ?view=roadmap, ?open=28,
// ?kind=story, ?spoilers=1 — which is how the entry's screenshots are
// framed, and how a reader can link straight to one trophy's guide.

import { createStore } from "./store.js";
import {
  KIND_LABEL,
  PHASE_TITLES,
  isShielded,
  renderDetail,
  renderMissableFeature,
  renderProgress,
  renderRoadmap,
  renderRow,
  renderSources,
} from "./render.js";

const doc = await fetch("data/trophies.json").then((r) => r.json());
const trophiesById = new Map(doc.trophies.map((t) => [t.id, t]));

const params = new URLSearchParams(location.search);
const ui = {
  view: params.get("view") ?? "tracker",
  kind: params.get("kind") ?? "all",
  grade: "all",
  query: "",
  hideEarned: false,
  selectedId: Number(params.get("open")) || null,
};

const store = createStore(() => refresh());

const listEl = document.getElementById("trophy-list");
const detailEl = document.getElementById("detail");
const emptyEl = document.getElementById("empty");
const resultEl = document.getElementById("result-count");
const chipsEl = document.getElementById("kind-chips");
const searchEl = document.getElementById("search");
const gradeEl = document.getElementById("grade-filter");
const spoilerEl = document.getElementById("spoiler-toggle");
const hideEarnedEl = document.getElementById("hide-earned");

/* ------------------------------ filters ------------------------------ */

const KINDS = ["all", ...Object.keys(KIND_LABEL)];
for (const kind of KINDS) {
  const chip = document.createElement("button");
  chip.type = "button";
  chip.className = "chip" + (ui.kind === kind ? " is-active" : "");
  chip.dataset.kind = kind;
  const count = kind === "all" ? doc.trophies.length : doc.trophies.filter((t) => t.kind === kind).length;
  chip.textContent = `${kind === "all" ? "All kinds" : KIND_LABEL[kind]} `;
  const n = document.createElement("span");
  n.className = "chip-n";
  n.textContent = String(count);
  chip.append(n);
  chip.addEventListener("click", () => {
    ui.kind = kind;
    for (const c of chipsEl.children) c.classList.toggle("is-active", c.dataset.kind === kind);
    refresh();
  });
  chipsEl.append(chip);
}

searchEl.addEventListener("input", () => {
  ui.query = searchEl.value.trim().toLowerCase();
  refresh();
});
gradeEl.addEventListener("change", () => {
  ui.grade = gradeEl.value;
  refresh();
});
spoilerEl.checked = store.state.spoilers;
spoilerEl.addEventListener("change", () => store.setSpoilers(spoilerEl.checked));
hideEarnedEl.addEventListener("change", () => {
  ui.hideEarned = hideEarnedEl.checked;
  refresh();
});

/* --------------------------- export / import --------------------------- */

document.getElementById("export-btn").addEventListener("click", () => {
  const blob = new Blob([store.exportJson()], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "leonida-legend-progress.json";
  a.click();
  URL.revokeObjectURL(url);
});
document.getElementById("import-file").addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  try {
    store.importJson(await file.text());
    spoilerEl.checked = store.state.spoilers;
  } catch {
    resultEl.textContent = "That file is not a Leonida Legend progress export — nothing was imported.";
  }
  event.target.value = "";
});
document.getElementById("reset-btn").addEventListener("click", () => {
  if (confirm("Reset the tracker? Every tick and counter goes back to zero.")) {
    store.reset();
    spoilerEl.checked = false;
  }
});

/* ------------------------------ view tabs ------------------------------ */

function showView(name) {
  ui.view = name;
  for (const tab of document.querySelectorAll(".view-tab")) {
    tab.classList.toggle("is-active", tab.dataset.view === name);
  }
  for (const section of document.querySelectorAll(".view")) {
    section.hidden = section.id !== `view-${name}`;
  }
}
for (const tab of document.querySelectorAll(".view-tab")) {
  tab.addEventListener("click", () => showView(tab.dataset.view));
}

/* ------------------------------- refresh ------------------------------- */

function matches(trophy) {
  if (ui.kind !== "all" && trophy.kind !== ui.kind) return false;
  if (ui.grade !== "all" && trophy.grade !== ui.grade) return false;
  if (ui.hideEarned && store.isEarned(trophy.id)) return false;
  if (ui.query) {
    if (isShielded(trophy, store)) return false;
    const haystack = `${trophy.name} ${trophy.description} ${trophy.guide} ${trophy.type}`.toLowerCase();
    if (!haystack.includes(ui.query)) return false;
  }
  return true;
}

function refresh() {
  renderProgress(
    doc,
    store,
    document.getElementById("overall-count"),
    document.getElementById("overall-pct"),
    document.getElementById("overall-fill"),
    document.getElementById("grade-progress"),
  );
  spoilerEl.checked = store.state.spoilers;

  const visible = doc.trophies.filter(matches);
  resultEl.textContent = `Showing ${visible.length} of ${doc.trophies.length} trophies · click any row for its full guide`;
  emptyEl.hidden = visible.length > 0;

  // Rows are grouped by roadmap phase, official-list order inside a phase.
  const ordered = [...visible].sort((a, b) => a.phase - b.phase || a.id - b.id);
  listEl.replaceChildren();
  let lastPhase = null;
  for (const trophy of ordered) {
    if (trophy.phase !== lastPhase) {
      lastPhase = trophy.phase;
      const head = document.createElement("div");
      head.className = "phase-head";
      const inPhase = doc.trophies.filter((t) => t.phase === lastPhase);
      const done = inPhase.filter((t) => store.isEarned(t.id)).length;
      const title = document.createElement("h3");
      title.textContent = PHASE_TITLES[lastPhase];
      const span = document.createElement("span");
      span.textContent = `${done} of ${inPhase.length} earned`;
      head.append(title, span);
      listEl.append(head);
    }
    listEl.append(
      renderRow(
        trophy,
        store,
        ui.selectedId,
        (id) => {
          ui.selectedId = id;
          refresh();
        },
        (id, earned) => store.setEarned(id, earned, trophiesById),
        trophiesById,
      ),
    );
  }

  const selected = ui.selectedId != null ? trophiesById.get(ui.selectedId) : ordered[0];
  renderDetail(detailEl, selected ?? null, store, trophiesById);
}

/* -------------------------------- boot -------------------------------- */

if (params.get("spoilers") === "1" && !store.state.spoilers) store.setSpoilers(true);
renderRoadmap(
  doc,
  document.getElementById("phases"),
  document.getElementById("stat-cards"),
  document.getElementById("roadmap-missable"),
);
renderMissableFeature(doc, document.getElementById("missable-feature"), store);
renderSources(doc, document.getElementById("about-text"), document.getElementById("bibliography"));
showView(ui.view);
refresh();
