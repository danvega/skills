// Build a HyperFrames `window.__TOKENS` blob from real source files.
//
// The vendored blocks render every token as a keyed <span> and FLIP between states: a token
// whose key exists in BOTH the previous and next state glides to its new position; a key that
// appears for the first time reads as added. So the key assignment IS the diff — get it wrong
// and the whole snippet re-types instead of the one changed line moving.
//
// States are chained: state N inherits keys from state N-1 via an LCS over token content.
//
// Usage:
//   node tokenize.mjs --seq diff --lang java --out tokens.json before.java after.java
//
//   --seq   the block's sequence key — must match window.__BLOCK.seq in the target block:
//             code-diff   → diff    (2 states)
//             code-typing → feature (1 state)
//             code-morph  → morph   (3 states)
//   --lang  any Shiki language id (java, kotlin, xml, properties, bash, json…)
//   --theme any Shiki theme id (default vitesse-dark — muted, sits well on the green card)

import { readFileSync, writeFileSync } from "node:fs";
import { createHighlighter } from "shiki";

const argv = process.argv.slice(2);
const opt = (name, fallback) => {
  const i = argv.indexOf(`--${name}`);
  return i === -1 ? fallback : argv[i + 1];
};
const seq = opt("seq", "diff");
const lang = opt("lang", "java");
const theme = opt("theme", "vitesse-dark");
const outPath = opt("out", "tokens.json");
const files = argv.filter((a, i) => !a.startsWith("--") && !argv[i - 1]?.startsWith("--"));

if (files.length === 0) {
  console.error("no source files given — pass one file per state, in order");
  process.exit(1);
}

const EXPECTED = { diff: 2, feature: 1, morph: 3 };
if (EXPECTED[seq] && files.length !== EXPECTED[seq]) {
  console.error(
    `--seq ${seq} expects ${EXPECTED[seq]} state file(s), got ${files.length}. ` +
      `The block's timeline is built around that count; a mismatch renders blank frames.`,
  );
  process.exit(1);
}

const hl = await createHighlighter({ themes: [theme], langs: [lang] });

// Flatten Shiki's line/token structure into the flat stream the blocks expect, with a literal
// "\n" token between lines (the block engine starts a new .line div on that exact content).
function flatten(code) {
  const { tokens: lines } = hl.codeToTokens(code, { lang, theme });
  const out = [];
  lines.forEach((line, i) => {
    if (i > 0) out.push({ content: "\n", color: "", fontStyle: 0 });
    for (const t of line) {
      out.push({ content: t.content, color: t.color ?? "#f4f7f2", fontStyle: t.fontStyle ?? 0 });
    }
  });
  return out;
}

// Longest common subsequence over token content. The pairs it returns are the tokens that
// survive the edit and should keep their identity.
function lcsPairs(a, b) {
  const n = a.length;
  const m = b.length;
  const dp = Array.from({ length: n + 1 }, () => new Uint32Array(m + 1));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[i][j] =
        a[i].content === b[j].content
          ? dp[i + 1][j + 1] + 1
          : Math.max(dp[i + 1][j], dp[i][j + 1]);
    }
  }
  const pairs = [];
  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (a[i].content === b[j].content) {
      pairs.push([i, j]);
      i++;
      j++;
    } else if (dp[i + 1][j] >= dp[i][j + 1]) i++;
    else j++;
  }
  return pairs;
}

const sources = files.map((f) => readFileSync(f, "utf8").replace(/\n$/, ""));
const states = sources.map((code) => ({ code, tokens: flatten(code) }));

// First state is all-original; each later state inherits a key wherever it matched the one before.
states[0].tokens.forEach((t, i) => (t.key = `s0-${i}`));
const carriedCounts = [];
for (let s = 1; s < states.length; s++) {
  const prev = states[s - 1].tokens;
  const cur = states[s].tokens;
  const carried = new Map(lcsPairs(prev, cur).map(([i, j]) => [j, prev[i].key]));
  cur.forEach((t, j) => (t.key = carried.get(j) ?? `s${s}-${j}`));
  carriedCounts.push(carried.size);
}

const { bg, fg } = hl.codeToTokens("", { lang, theme });
writeFileSync(
  outPath,
  JSON.stringify(
    { [seq]: { lang, theme, bg: bg ?? "#0d110a", fg: fg ?? "#f4f7f2", states } },
    null,
    2,
  ),
);

console.log(
  `${seq}: ${states.map((s) => `${s.tokens.length} tokens`).join(" → ")}` +
    (carriedCounts.length ? ` · carried (glide): ${carriedCounts.join(", ")}` : ""),
);
