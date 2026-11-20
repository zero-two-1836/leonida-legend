#!/usr/bin/env node
// Take the 4 screenshots listed in shots.json: real renders of app/ in
// headless Chromium (Playwright), viewport 1280x800, saved as JPEG into
// screenshots/. A fixed demo progress state is seeded into localStorage
// first — the same earned set and counters every run — so the shots are
// deterministic: same input state, same render, same bytes near enough
// that the dossier rebuild is stable.
//
//   node serve.ts --port 8940 &        (in another shell)
//   node tools/take-screenshots.mjs

import { chromium } from "/home/hatch/workspace/makefun-gta6/node_modules/playwright/index.mjs";
import { readFileSync } from "node:fs";

const BASE = "http://localhost:8940";
const STORAGE_KEY = "leonida-legend-progress-v1";

// A plausible mid-run state: the opening of the story done, a few
// activities banked, counters under way — 14 trophies earned.
const DEMO = {
  earned: [2, 3, 8, 16, 18, 19, 20, 21, 24, 33, 36, 39, 41, 51],
  counters: { 15: 163, 17: 31, 28: 11, 30: 1, 31: 64, 32: 27, 35: 72, 48: 210, 52: 90000, 53: 61000 },
  spoilers: false,
};

const shots = JSON.parse(readFileSync(new URL("../shots.json", import.meta.url), "utf-8"));

const browser = await chromium.launch({ args: ["--no-sandbox"] });
for (const shot of shots) {
  const context = await browser.newContext({ viewport: shot.viewport });
  const page = await context.newPage();
  await page.goto(BASE + "/", { waitUntil: "networkidle" });
  await page.evaluate(
    ([key, value]) => localStorage.setItem(key, JSON.stringify(value)),
    [STORAGE_KEY, DEMO],
  );
  await page.goto(BASE + shot.path, { waitUntil: "networkidle" });
  await page.waitForSelector(shot.path.includes("view=roadmap") ? ".phase-card" : ".trow", { timeout: 10000 });
  const open = new URLSearchParams(shot.path.split("?")[1] ?? "").get("open");
  if (open) {
    // Centre the opened trophy's row inside the list's own scroll box —
    // deliberately not scrollIntoView, which would also scroll the page
    // and push the filter controls out of the frame.
    await page.evaluate((id) => {
      const list = document.querySelector(".trophy-list");
      const row = document.querySelector(`[data-id="${id}"]`);
      if (!list || !row) return;
      const listRect = list.getBoundingClientRect();
      const rowRect = row.getBoundingClientRect();
      list.scrollTop += rowRect.top - listRect.top - (listRect.height - rowRect.height) / 2;
    }, open);
  }
  await page.waitForTimeout(500);
  await page.screenshot({ path: new URL(`../screenshots/${shot.file}`, import.meta.url).pathname, type: "jpeg", quality: 88 });
  console.log("shot", shot.file, "ok");
  await context.close();
}
await browser.close();
