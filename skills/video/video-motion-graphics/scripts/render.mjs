// Deterministic HTML capture. See references/rendering.md for the CLI and cache contract.
import { chromium } from "playwright";
import { mkdirSync, readFileSync, writeFileSync, existsSync, readdirSync, unlinkSync, renameSync, statSync } from "node:fs";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { resolve, dirname } from "node:path";
import { pathToFileURL } from "node:url";
import { parseFps, positive } from "./render-options.mjs";

const arg = (name, fallback) => {
  const i = process.argv.indexOf(`--${name}`);
  return i < 0 ? fallback : process.argv[i + 1];
};
const flag = name => process.argv.includes(`--${name}`);
const hash = value => createHash("sha256").update(value).digest("hex");
const readJSON = path => {
  try { return JSON.parse(readFileSync(path, "utf8")); } catch { return null; }
};

async function main() {
  if (!arg("template")) throw new Error("--template is required");
  const template = resolve(arg("template"));
  const params = JSON.parse(arg("params-file") ? readFileSync(arg("params-file"), "utf8") : arg("params", "{}"));
  const duration = positive(arg("duration", "6"), "duration", 7200);
  const fps = parseFps(arg("fps", "30"));
  const scale = positive(arg("scale", "1"), "scale", 4);
  const width = positive(arg("width", "1920"), "width", 7680, true);
  const height = positive(arg("height", "1080"), "height", 7680, true);
  const frames = Math.max(1, Math.round(duration * fps.rate));
  if (frames > 500000) throw new Error("Render exceeds 500,000 frames; split it into shorter clips");
  if (!Number.isInteger(width * scale) || !Number.isInteger(height * scale)) throw new Error("Raster dimensions must be integers");
  const outDir = resolve(arg("out", "frames"));
  const mov = arg("mov") ? resolve(arg("mov")) : null;
  const poster = arg("poster") ? resolve(arg("poster")) : null;
  const at = Number(arg("at", String(duration / 2)));
  if (!Number.isFinite(at) || at < 0 || at >= duration) throw new Error("--at must fall within the clip");
  if (poster && mov) throw new Error("--poster and --mov are separate output modes");
  // Self-contained HTML is the normal contract. List mutable local assets with --dependency.
  const dependencies = process.argv.flatMap((v, i) => v === "--dependency" ? [process.argv[i + 1]] : []);
  const dependencyHashes = dependencies.map(p => [resolve(p), hash(readFileSync(p))]);
  const started = performance.now();
  const browser = await chromium.launch({ channel: "chrome" });
  let key;
  let cached = false;
  try {
    key = hash(JSON.stringify({ version: 2, html: hash(readFileSync(template)), template,
      params, duration, fps: fps.ffmpeg, scale, width, height, dependencyHashes, browser: browser.version() }));
    const receipt = readJSON(`${outDir}/render.json`);
    cached = !poster && !flag("no-cache") && receipt?.key === key && receipt.frames === frames &&
      Array.from({ length: frames }, (_, i) => `${outDir}/f_${String(i).padStart(4, "0")}.png`)
        .every(p => existsSync(p) && statSync(p).size > 0);
    if (!cached) {
      const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: scale });
      await page.goto(pathToFileURL(template).href);
      await page.evaluate(async p => {
        if (typeof window.seek !== "function" || typeof window.setParams !== "function") throw new Error("Template must implement setParams and seek");
        window.setParams(p);
        await document.fonts.ready;
        await Promise.all([...document.images].filter(im => im.getAttribute("src")).map(im => im.decode()));
      }, params);
      if (poster) {
        mkdirSync(dirname(poster), { recursive: true });
        await page.evaluate(([t, d]) => window.seek(t, d), [at, duration]);
        await page.screenshot({ path: poster, omitBackground: true });
      } else {
        mkdirSync(outDir, { recursive: true });
        // Remove only this renderer's frames and receipt. A shorter revision must not retain a tail.
        for (const file of readdirSync(outDir)) {
          if (/^f_\d+\.png$/.test(file) || file === "render.json") unlinkSync(`${outDir}/${file}`);
        }
        for (let i = 0; i < frames; i++) {
          await page.evaluate(([t, d]) => window.seek(t, d), [i / fps.rate, duration]);
          await page.screenshot({ path: `${outDir}/f_${String(i).padStart(4, "0")}.png`, omitBackground: true });
        }
        writeFileSync(`${outDir}/render.json`, JSON.stringify({ key, frames, fps: fps.ffmpeg,
          requestedDuration: duration, encodedDuration: frames / fps.rate, width: width * scale,
          height: height * scale }, null, 2));
      }
    }
  } finally { await browser.close(); }

  if (mov) {
    const receipt = readJSON(`${mov}.json`);
    const reusable = cached && existsSync(mov) && receipt?.key === key && receipt.size === statSync(mov).size && receipt.mtimeMs === statSync(mov).mtimeMs;
    if (!reusable) {
      mkdirSync(dirname(mov), { recursive: true });
      const temporary = `${mov}.partial.mov`;
      const r = spawnSync("ffmpeg", ["-nostdin", "-y", "-v", "error", "-framerate", fps.ffmpeg,
        "-i", `${outDir}/f_%04d.png`, "-frames:v", String(frames), "-c:v", "prores_ks",
        "-profile:v", "4444", "-pix_fmt", "yuva444p10le", temporary], { stdio: "inherit" });
      if (r.status !== 0) throw new Error(`ffmpeg encode failed: ${r.error?.message ?? r.status}`);
      renameSync(temporary, mov);
      writeFileSync(`${mov}.json`, JSON.stringify({ key, size: statSync(mov).size, mtimeMs: statSync(mov).mtimeMs }));
    }
  }
  console.log(JSON.stringify({ output: poster ?? mov ?? outDir, cacheHit: cached, frames: poster ? 1 : frames,
    fps: fps.ffmpeg, seconds: Number(((performance.now() - started) / 1000).toFixed(2)) }));
}
main().catch(error => { console.error(error.message); process.exitCode = 1; });
