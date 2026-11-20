// Rendering for Leonida Legend: the tracker rows and guide pane, the
// roadmap, the missables briefing and the bibliography. Pure DOM building
// from the data file and the progress store — no framework, no network.

export const GRADE_ORDER = ["platinum", "gold", "silver", "bronze"];
export const GRADE_LABEL = { platinum: "PLATINUM", gold: "GOLD", silver: "SILVER", bronze: "BRONZE" };
export const KIND_LABEL = {
  story: "Story",
  side: "Side strands",
  missable: "Missable",
  collectibles: "Collectibles",
  activities: "Activities",
  cleanup: "Cleanup",
};
export const PHASE_TITLES = {
  1: "Phase 1 · Story",
  2: "Phase 2 · The 100% engine",
  3: "Phase 3 · Collectibles & world",
  4: "Phase 4 · Strangers",
  5: "Phase 5 · Crime, money & feats",
};

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text != null) node.textContent = text;
  return node;
}

export function formatCount(n, prefix = "") {
  return prefix + n.toLocaleString("en-US");
}

// A story trophy is shielded when the spoiler shield is on and it is not
// yet earned: name, description and guide all stay hidden, per the bounty.
export function isShielded(trophy, store) {
  return store.state.spoilers && trophy.kind === "story" && !store.isEarned(trophy.id);
}

export function gradeBadge(grade) {
  return el("span", `grade grade-${grade}`, GRADE_LABEL[grade]);
}

function sourcesBlock(trophy) {
  const wrap = el("div", "sources");
  wrap.append(el("strong", null, "Sources: "));
  trophy.sources.forEach((source, i) => {
    if (i > 0) wrap.append(document.createTextNode(" · "));
    if (source.url) {
      const a = el("a", null, source.name);
      a.href = source.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      wrap.append(a);
    } else {
      wrap.append(document.createTextNode(source.name));
    }
  });
  return wrap;
}

function counterBox(trophy, store, trophiesById) {
  const box = el("div", "counter-box");
  const value = store.counterOf(trophy.id);
  box.append(el("span", "c-label", `Progress: ${formatCount(value, trophy.countPrefix ?? "")} / ${formatCount(trophy.count, trophy.countPrefix ?? "")}`));
  const minus = el("button", null, "−");
  minus.type = "button";
  minus.title = "One less";
  minus.addEventListener("click", () => store.setCounter(trophy.id, value - (trophy.countStep ?? 1), trophiesById));
  const input = document.createElement("input");
  input.type = "number";
  input.min = "0";
  input.value = String(value);
  input.setAttribute("aria-label", `Count for ${trophy.name}`);
  input.addEventListener("change", () => store.setCounter(trophy.id, input.value, trophiesById));
  const plus = el("button", null, "+");
  plus.type = "button";
  plus.title = "One more";
  plus.addEventListener("click", () => store.setCounter(trophy.id, value + (trophy.countStep ?? 1), trophiesById));
  box.append(minus, input, plus);
  return box;
}

/* ------------------------------ tracker ------------------------------ */

export function renderRow(trophy, store, selectedId, onSelect, onToggle, trophiesById) {
  const shielded = isShielded(trophy, store);
  const row = el("div", "trow" + (store.isEarned(trophy.id) ? " is-earned" : "") + (trophy.id === selectedId ? " is-selected" : ""));
  row.dataset.id = String(trophy.id);
  row.setAttribute("role", "button");
  row.setAttribute("tabindex", "0");

  const tick = el("span", "tick");
  const box = document.createElement("input");
  box.type = "checkbox";
  box.checked = store.isEarned(trophy.id);
  box.setAttribute("aria-label", `Mark ${trophy.name} as earned`);
  box.addEventListener("click", (event) => event.stopPropagation());
  box.addEventListener("change", () => onToggle(trophy.id, box.checked));
  tick.append(box);

  const main = el("span");
  main.append(el("span", "tname", shielded ? "Hidden trophy" : trophy.name));
  main.append(el("span", "tdesc", shielded ? "A story trophy, shielded until earned." : trophy.description));

  const meta = el("span", "tmeta");
  meta.append(el("span", null, trophy.type));
  meta.append(el("span", null, trophy.time));
  if (trophy.count) {
    const done = store.counterOf(trophy.id);
    meta.append(el("span", "count-progress", `${formatCount(done, trophy.countPrefix ?? "")} / ${formatCount(trophy.count, trophy.countPrefix ?? "")}`));
  }
  if (trophy.missable) {
    const flag = el("span", "tag tag-missable", "MISSABLE");
    meta.append(flag);
  }

  row.append(tick, gradeBadge(trophy.grade), main, meta);
  row.addEventListener("click", () => onSelect(trophy.id));
  row.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelect(trophy.id);
    }
  });
  return row;
}

export function renderDetail(pane, trophy, store, trophiesById) {
  pane.replaceChildren();
  if (!trophy) {
    pane.append(el("p", "detail-empty", "Pick a trophy on the left and its full guide — steps, pitfalls, time and sources — opens here."));
    return;
  }
  const shielded = isShielded(trophy, store);

  const gradeRow = el("div", "d-grade-row");
  gradeRow.append(gradeBadge(trophy.grade));
  gradeRow.append(el("span", "tag", trophy.type));
  gradeRow.append(el("span", "tag", PHASE_TITLES[trophy.phase]));
  if (trophy.hidden) gradeRow.append(el("span", "tag tag-hidden", "Hidden on PSN"));
  pane.append(gradeRow);

  if (trophy.missable) {
    pane.append(el("div", "missable-banner", "⚠ MISSABLE — this one can be lost. Read the warning before you play on."));
  }

  pane.append(el("h2", null, shielded ? "Hidden trophy" : trophy.name));
  const official = el("p", "d-official");
  official.append(el("em", null, shielded ? "Shielded by the spoiler shield until earned." : `“${trophy.description}”`));
  official.append(document.createTextNode(shielded ? "" : " — official PlayStation description"));
  pane.append(official);

  if (shielded) {
    pane.append(el("p", "shield-note", "The spoiler shield is on: this story trophy's name, description and guide stay hidden until you earn it. Its grade, kind and roadmap phase still show, so the run stays plannable."));
    return;
  }

  const tags = el("div", "d-tags");
  tags.append(el("span", "tag", `Time: ${trophy.time}`));
  if (trophy.count) tags.append(el("span", "tag", `Tracked count: ${formatCount(trophy.count, trophy.countPrefix ?? "")}`));
  pane.append(tags);

  pane.append(el("h4", null, "The guide"));
  pane.append(el("p", null, trophy.guide));

  pane.append(el("h4", null, "Step by step"));
  const steps = el("ol", "steps");
  for (const step of trophy.steps) steps.append(el("li", null, step));
  pane.append(steps);

  if (trophy.watchout) {
    const warn = el("div", "watchout");
    warn.append(el("strong", null, "Watch out: "));
    warn.append(document.createTextNode(trophy.watchout));
    pane.append(warn);
  }

  if (trophy.count) pane.append(counterBox(trophy, store, trophiesById));

  const earnRow = el("label", "earn-row");
  const earnBox = document.createElement("input");
  earnBox.type = "checkbox";
  earnBox.checked = store.isEarned(trophy.id);
  earnBox.addEventListener("change", () => store.setEarned(trophy.id, earnBox.checked, trophiesById));
  earnRow.append(earnBox, document.createTextNode("Earned — tick it off"));
  pane.append(earnRow);

  pane.append(sourcesBlock(trophy));
}

/* ------------------------------ roadmap ------------------------------ */

export function renderRoadmap(doc, phasesEl, statsEl, alertEl) {
  statsEl.replaceChildren();
  const stats = [
    ["4 / 10", "Difficulty (PowerPyx)"],
    ["~200 h", "To platinum (PowerPyx)"],
    ["1", "Playthrough needed"],
    ["1", "Missable trophy"],
    ["0", "Online trophies"],
    ["28", "Hidden on PSN"],
  ];
  for (const [value, label] of stats) {
    const card = el("div", "stat-card");
    card.append(el("span", "stat-v", value), el("span", "stat-k", label));
    statsEl.append(card);
  }

  alertEl.replaceChildren();
  const strong = el("strong", null, "MISSABLE — Positive Mental Attitude: ");
  alertEl.append(strong, document.createTextNode(doc.missableNote));

  phasesEl.replaceChildren();
  for (const phase of doc.roadmap) {
    const card = el("li", "phase-card");
    card.append(el("div", "phase-num", String(phase.phase)));
    const body = el("div");
    body.append(el("h3", null, phase.title));
    body.append(el("span", "phase-hours", phase.hours));
    body.append(el("p", null, phase.text));
    const chips = el("div", "phase-trophies");
    for (const trophy of doc.trophies.filter((t) => t.phase === phase.phase)) {
      chips.append(el("span", "tag", trophy.name));
    }
    body.append(chips);
    card.append(body);
    phasesEl.append(card);
  }
}

/* ----------------------------- missables ----------------------------- */

export function renderMissableFeature(doc, host, store) {
  const trophy = doc.trophies.find((t) => t.missable);
  host.replaceChildren();
  const card = el("article", "missable-feature-card");
  const gradeRow = el("div", "d-grade-row");
  gradeRow.append(gradeBadge(trophy.grade), el("span", "tag tag-missable", "THE ONE MISSABLE"), el("span", "tag", trophy.type));
  card.append(gradeRow);
  card.append(el("h3", null, trophy.name));
  const official = el("p", "d-official");
  official.append(el("em", null, `“${trophy.description}”`), document.createTextNode(" — official PlayStation description"));
  card.append(official);
  card.append(el("p", null, trophy.guide));
  const steps = el("ol", "steps");
  for (const step of trophy.steps) steps.append(el("li", null, step));
  card.append(steps);
  const warn = el("div", "watchout");
  warn.append(el("strong", null, "Watch out: "), document.createTextNode(trophy.watchout));
  card.append(warn);
  card.append(sourcesBlock(trophy));
  host.append(card);
}

/* ------------------------------ sources ------------------------------ */

const SOURCE_USE = {
  "PlayStation's official": "The authority for every name, description, grade and tracked count in the tracker.",
  PSNProfiles: "The same official list in tracker form; used for rarity context and count checks.",
  Exophase: "A second listing of the official list; used to cross-check names and grades.",
  PowerPyx: "Roadmap shape, the 4/10 difficulty and ~200-hour estimates, the missable flag and most method notes.",
  SixShore: "The hidden/non-hidden split (28 hidden), per-trophy method confirmations and the looks-missable list.",
  GTADB: "A cross-checked trophy list and platinum overview; a third agreement on the 55 names.",
  EGamers: "The hidden trophy split by grade, used to check the 28 count.",
};

export function renderSources(doc, aboutEl, bibEl) {
  aboutEl.textContent = doc.about;
  const seen = new Map();
  for (const trophy of doc.trophies) {
    for (const source of trophy.sources) {
      if (!seen.has(source.name)) seen.set(source.name, source);
    }
  }
  bibEl.replaceChildren();
  for (const source of seen.values()) {
    const item = el("li");
    if (source.url) {
      const a = el("a", null, source.name);
      a.href = source.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      item.append(a);
    } else {
      item.append(el("strong", null, source.name));
    }
    const use = Object.entries(SOURCE_USE).find(([key]) => source.name.startsWith(key));
    if (use) item.append(el("span", "bib-use", use[1]));
    bibEl.append(item);
  }
}

/* ------------------------------ progress ------------------------------ */

export function renderProgress(doc, store, countEl, pctEl, fillEl, gradesEl) {
  const earned = doc.trophies.filter((t) => store.isEarned(t.id)).length;
  countEl.textContent = `${earned} of ${doc.trophies.length} earned`;
  const pct = Math.round((earned / doc.trophies.length) * 100);
  pctEl.textContent = `${pct}%`;
  fillEl.style.width = `${pct}%`;
  gradesEl.replaceChildren();
  for (const grade of GRADE_ORDER) {
    const all = doc.trophies.filter((t) => t.grade === grade);
    const got = all.filter((t) => store.isEarned(t.id)).length;
    const item = el("span", "gp");
    const dot = el("span", "dot");
    dot.style.background = `var(--${grade})`;
    item.append(dot, document.createTextNode(`${GRADE_LABEL[grade][0] + GRADE_LABEL[grade].slice(1).toLowerCase()} — ${got}/${all.length}`));
    gradesEl.append(item);
  }
}
