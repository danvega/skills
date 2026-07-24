// Render a motion-graphics template to transparent PNG frames (and optionally a ProRes 4444 .mov).
//
// Usage:
//   node render.mjs --template <path.html> --duration 6 --out <framesDir> \
//        [--params '{"name":"Dan Vega","role":"Spring Developer Advocate"}'] \
//        [--fps 30] [--mov <overlay.mov>]
//
// Templates must implement window.setParams(obj) and window.seek(t, total).
// Uses the system Chrome via Playwright (channel: "chrome") — no browser download needed.

import { chromium } from "playwright";
import { mkdirSync } from "fs";
import { spawnSync } from "child_process";
import { resolve } from "path";

const arg = (name, def) => {
  const i = process.argv.indexOf("--" + name);
  return i > -1 ? process.argv[i + 1] : def;
};

const template = arg("template");
if (!template) { console.error("--template is required"); process.exit(1); }
const params   = JSON.parse(arg("params", "{}"));
const duration = parseFloat(arg("duration", "6"));
const fps      = parseInt(arg("fps", "30"), 10);
const outDir   = resolve(arg("out", "frames"));
const mov      = arg("mov", null);
const scale    = parseFloat(arg("scale", "1")); // deviceScaleFactor: 2 => 4K raster from the 1080 layout
const width    = parseInt(arg("width", "1920"), 10);  // e.g. 1080x1920 for 9:16 shorts captions
const height   = parseInt(arg("height", "1080"), 10);

mkdirSync(outDir, { recursive: true });

const browser = await chromium.launch({ channel: "chrome" });
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: scale });
await page.goto("file://" + resolve(template));
await page.waitForTimeout(300); // fonts
await page.evaluate(p => window.setParams && window.setParams(p), params);

const frames = Math.round(duration * fps);
for (let i = 0; i < frames; i++) {
  await page.evaluate(([t, d]) => window.seek(t, d), [i / fps, duration]);
  await page.screenshot({
    path: `${outDir}/f_${String(i).padStart(4, "0")}.png`,
    omitBackground: true,
  });
}
await browser.close();
console.log(`rendered ${frames} frames -> ${outDir}`);

if (mov) {
  const r = spawnSync("ffmpeg", [
    "-y", "-v", "error",
    "-framerate", String(fps), "-i", `${outDir}/f_%04d.png`,
    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le",
    mov,
  ], { stdio: "inherit" });
  if (r.status !== 0) process.exit(r.status ?? 1);
  console.log(`encoded ${mov}`);
}
