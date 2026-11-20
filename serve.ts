// A pocket static server for trying the guide locally.
//
//   node serve.ts               serves app/ at http://localhost:8080
//   node serve.ts --port 9090   serves it on another port
//
// Standard library only. It answers each request with the file of the
// same path under app/ (index.html for a folder), with a content type a
// browser understands, and refuses every path that climbs out of app/.
// The guide needs no server at all — any static host will do — this one
// only exists so the app can be previewed with a single command.

import { createReadStream, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize, resolve, sep } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = resolve(fileURLToPath(new URL("./app", import.meta.url)));

const args = process.argv.slice(2);
const portAt = args.indexOf("--port");
const wanted = portAt === -1 ? 8080 : Number(args[portAt + 1]);
const port = Number.isInteger(wanted) && wanted > 0 && wanted < 65536 ? wanted : 8080;

const TYPES: Record<string, string> = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".mjs": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".ico": "image/x-icon",
  ".woff2": "font/woff2",
};

function fail(res: import("node:http").ServerResponse, status: number, text: string) {
  res.writeHead(status, { "content-type": "text/plain; charset=utf-8" });
  res.end(text);
}

createServer((req, res) => {
  let path: string;
  try {
    path = decodeURIComponent(new URL(req.url ?? "/", "http://localhost").pathname);
  } catch {
    fail(res, 400, "bad request");
    return;
  }
  if (path.endsWith("/")) path += "index.html";

  const file = resolve(join(appRoot, normalize(path)));
  if (file !== appRoot && !file.startsWith(appRoot + sep)) {
    fail(res, 403, "forbidden");
    return;
  }

  let size: number;
  try {
    const info = statSync(file);
    if (!info.isFile()) throw new Error("not a file");
    size = info.size;
  } catch {
    fail(res, 404, "not found");
    return;
  }

  res.writeHead(200, {
    "content-type": TYPES[extname(file).toLowerCase()] ?? "application/octet-stream",
    "content-length": size,
  });
  createReadStream(file).pipe(res);
}).listen(port, "127.0.0.1", () => {
  console.log(`Leonida Legend is open at http://localhost:${port}`);
});
