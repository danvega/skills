// Restyle a vendored HyperFrames block into the channel's terminal design language, size the
// editor card to the snippet, and splice in the tokens from tokenize.mjs.
//
// The blocks' animation engine is never touched — this is a CSS token swap plus one splice, so
// a vendored block stays diffable against upstream.
//
// Usage:
//   node build.mjs --block ../assets/blocks/code-diff.html --tokens tokens.json \
//                  --out proj/index.html --filename UserController.java [--transparent]
//
// --transparent drops the full-frame background layers so only the card composites, for the
// alpha overlay render (see SKILL.md — the WebM needs format=yuva420p on the ffmpeg side).

import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

const argv = process.argv.slice(2);
const opt = (n, d) => {
  const i = argv.indexOf(`--${n}`);
  return i === -1 ? d : argv[i + 1];
};
const blockPath = opt("block");
const tokensPath = opt("tokens");
const outPath = opt("out");
const filename = opt("filename", "Example.java");
const transparent = argv.includes("--transparent");

let h = readFileSync(blockPath, "utf8");
const blob = JSON.parse(readFileSync(tokensPath, "utf8"));
const seq = Object.keys(blob)[0];
const states = blob[seq].states;

// The blocks hardcode a 1380x800 editor whatever the content is, which leaves most of the card
// empty for a short snippet. Size it to the code instead.
const lineCount = Math.max(...states.map((s) => s.code.split("\n").length));
const longest = Math.max(...states.flatMap((s) => s.code.split("\n").map((l) => l.length)));

const TITLEBAR = 56;
const CODE_TOP = 38;
const LINE_H = 46;
const PAD_BOTTOM = 34;
// 30px SF Mono advances ~18.05px. Budget the line-number gutter (104) + right padding (44) AND
// the diff chrome (22px sign + 14px indent) that only appears on changed lines — forget the
// chrome and the longest changed line clips off the right edge.
const CHROME = 104 + 44 + 22 + 14;

const editorH = TITLEBAR + CODE_TOP + lineCount * LINE_H + PAD_BOTTOM;
const editorW = Math.min(1380, Math.max(900, Math.round(longest * 18.05) + CHROME + 40));

const swaps = [
  // page + background field
  ["background: #05070b;", `background: ${transparent ? "transparent" : "#080b07"};`],
  [
    "radial-gradient(1200px 700px at 50% 18%, #0e1726 0%, #070b12 55%, #05070b 100%)",
    "radial-gradient(1200px 700px at 50% 18%, #16210f 0%, #0a0e08 55%, #080b07 100%)",
  ],
  [/rgba\(88, 166, 255, 0\.05\)/g, "rgba(140, 233, 154, 0.06)"],
  ["background: #1f6feb55;", "background: #8ce99a33;"],
  ["background: #2ea04355;", "background: #69db7c2e;"],

  // editor card — brand card bg, border, radius, sized to the snippet
  ["width: 1380px;", `width: ${editorW}px;`],
  ["height: 800px;", `height: ${editorH}px;`],
  ["background: #0b0f17;", "background: rgba(13, 17, 10, 0.92);"],
  ["border: 1px solid #1d2733;", "border: 1px solid rgba(255, 255, 255, 0.1);"],
  ["border-radius: 16px;", "border-radius: 14px;"],
  ["background: linear-gradient(#11161f, #0c111a);", "background: rgba(9, 12, 7, 0.96);"],
  ["border-bottom: 1px solid #1b2430;", "border-bottom: 1px solid rgba(255, 255, 255, 0.08);"],

  // type
  ['font-family: "JetBrains Mono", monospace;', 'font-family: "SF Mono", Menlo, monospace;'],
  ["color: #e6edf3;", "color: #f4f7f2;"],
  ["color: #8b98a9;", "color: rgba(255, 255, 255, 0.38);"],
  ["color: #d6e2f0;", "color: #8ce99a;"],
  ["color: #828c9b;", "color: rgba(255, 255, 255, 0.26);"],

  // caret + highlight band → green accent
  [/#58a6ff/g, "#69db7c"],
  ["rgba(88, 166, 255, 0.16)", "rgba(140, 233, 154, 0.14)"],

  // upstream ships a registry comment ahead of the doctype, which trips their own StaticGuard
  [/^<!--\s*hyperframes-registry-item:.*?-->\n/, ""],
];

const misses = [];
for (const [from, to] of swaps) {
  // Test for the pattern rather than comparing before/after — a swap can legitimately be a
  // no-op (e.g. a computed width that lands back on the block's own 1380px) and that is not
  // an upstream drift.
  const found = typeof from === "string" ? h.includes(from) : from.test(h);
  if (!found) misses.push(String(from));
  else h = h.replace(from, to);
}
if (misses.length) {
  console.warn(
    `  ! ${misses.length} brand swap(s) did not match — upstream block CSS may have changed:`,
  );
  misses.forEach((m) => console.warn(`    ${m}`));
}

// Title bar filename. Each block ships its own placeholder, so match on the element.
h = h.replace(
  /<span class="filename">.*?<\/span>\s*(?=<\/div>)/s,
  `<span class="filename"><span class="accent">${filename}</span></span>`,
);

if (transparent) {
  h = h.replace(/<div class="bg-(?:field|grid|glow a|glow b)"[^>]*><\/div>\s*/g, "");
}

// Splice the generated tokens over the block's baked-in literal.
const i = h.indexOf("window.__TOKENS");
const start = h.indexOf("{", i);
let depth = 0;
let end = -1;
for (let j = start; j < h.length; j++) {
  if (h[j] === "{") depth++;
  else if (h[j] === "}" && --depth === 0) {
    end = j + 1;
    break;
  }
}
h = h.slice(0, start) + JSON.stringify(blob, null, 2) + h.slice(end);

mkdirSync(dirname(outPath), { recursive: true });
writeFileSync(outPath, h);
console.log(`built ${outPath} · ${editorW}x${editorH} card · ${lineCount} lines`);
