// Leonida Legend — hand-in program for the gta6-trophy-guide-01 bounty.
//
// The entry itself is the static web app under app/: open app/index.html
// from any static server and the guide runs, fully offline. This program
// does the handing in. It copies app/ and screenshots/ into the output
// directory and writes dossier.json — the file the judge reads — using
// the vendored make.fun library, so the dossier it writes is byte for
// byte the one the scorer rebuilds from the same files.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// MAKEFUN_OUTPUT_DIR stands in for /output outside the grading sandbox.
// To try the guide itself instead: node serve.ts

import { cpSync, existsSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { buildDossier } from "./vendor/makefun-frontend.ts";

const here = fileURLToPath(new URL(".", import.meta.url));
const out = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

// The whole app goes in as-is: pages, styles, scripts and the data file.
mkdirSync(out, { recursive: true });
cpSync(join(here, "app"), join(out, "app"), { recursive: true });

// The screenshots travel under their own folder.
const shots = join(here, "screenshots");
if (existsSync(shots)) {
  mkdirSync(join(out, "screenshots"), { recursive: true });
  cpSync(shots, join(out, "screenshots"), { recursive: true });
}

// The dossier, built under this bounty's caps: source text to 160 KiB,
// at most 4 screenshots of at most 256 KiB each, app/ to 993 entries and
// 48 MiB. vendor/makefun-frontend.ts is the kit's library and is used
// unchanged on purpose — the gate rebuilds the dossier with its own copy
// and compares the two byte for byte.
const dossier = buildDossier(out, {
  text_max_bytes: 163840,
  screenshots: { max: 4, max_bytes: 262144 },
  app_max_files: 993,
  app_max_bytes: 50331648,
});
writeFileSync(join(out, "dossier.json"), dossier);
