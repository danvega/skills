---
name: video-code-animation
description: >-
  Render full-frame animated code inserts for a YouTube video — before/after diffs where only the
  changed tokens move, typed-in snippets, and multi-step refactor morphs — from real source files,
  in the channel's terminal design language, via the HyperFrames renderer. Delivers an MP4 insert, or an alpha overlay when needed. Use when Dan says "animate this code", "show the before and after",
  "animate the diff", "make the code type itself", "show this refactor", or wants a code change to
  read as motion instead of a screen recording. Do NOT use for cards/lower-thirds/zooms over
  existing footage (video-motion-graphics), cutting (video-rough-cut), captions or vertical clips
  (video-shorts), or thumbnails (video-packaging).
---

# Code Animation

Turn a code change into a full-frame animated insert. The camera never sees an editor — the
snippet is rendered from real source files, so the frame is clean, the type is huge, and the
*only* thing that moves is what actually changed.

This is the sibling to `video-motion-graphics`. That skill decorates footage Dan recorded; this
one produces footage that didn't exist. Both can use a visual plan from `video-visual-story` after `video-rough-cut`.

**Scope gate.** An animated insert earns its place when the change is small and the point is
"look what moved". A whole file scrolling past is not an animation, it's a screen recording —
use the real screen-share and put a `spotlight` on it (`video-motion-graphics`). Rule of thumb:
if the snippet is over ~14 lines, cut it down or don't animate it.

## Inputs

- **Two (or one, or three) source files** — one per state, in order. Real, compilable snippets
  trimmed to the lines that matter. Write them to the scratch dir; they are fixtures, not repo code.
- Optional: the video's transcript, to place the insert at the moment Dan describes the change.

Keep editable states, tokens, HTML, and previews in the project's
`03_Graphics/code-animation/<name>/`. Use a `cache/` subfolder for regenerable frames.
With no project, use `<source_dir>/video-code-animation/<name>/`. Resolve the rough cut's
`00_Project/edit/transcript.output.json` for timing; record the manifest ID in the visual plan.

## Block library

Vendored under `assets/blocks/` from the HeyGen HyperFrames registry (Apache 2.0), pinned at
`hyperframes@0.7.77`. Kept as unmodified upstream files — all branding is applied at build time
by `scripts/build.mjs`, so a block stays diffable when upstream changes.

| Block | `--seq` | States | Duration | Status | What it is |
|---|---|---|---|---|---|
| `code-diff.html` | `diff` | 2 | 6s | ✅ approved 2026-07-28 | before → after; removed lines collapse red, added expand green, unchanged tokens glide |
| `code-typing.html` | `feature` | 1 | 5s | ✅ approved 2026-07-28 | snippet types itself in with a tracking caret and line numbers |
| `code-morph.html` | `morph` | 3 | 7s | ✅ approved 2026-07-28 | one snippet becomes another, twice — for a 3-step refactor progression |

New blocks get approved the way these did: `npx hyperframes@0.7.77 add <name> --dir <tmp>`, check
it shares the same CSS shell (`grep "width: 1380px"` etc.), vendor it, render a real snippet, show
Dan, then add a dated row.

**Pick by intent**, not by novelty:
- Dan says "here's the change" → `code-diff`
- Dan is introducing a new API for the first time → `code-typing`
- Dan is walking a migration through stages (RestTemplate → RestClient → `@HttpExchange`) → `code-morph`

## Step 0 — One-time setup per machine

```bash
cd <skill>/scripts && npm ci
```

Requires Node 22+ and ffmpeg (both already on Dan's machine). The renderer downloads a headless
Chrome into `~/.cache/puppeteer` on first run. Verify with `npx hyperframes@0.7.77 doctor` — the
whisper / TTS / MusicGen misses are optional and irrelevant here.

Turn off their telemetry once: `npx hyperframes@0.7.77 telemetry disable`.

## Step 1 — Write the state files

One file per state, real code, trimmed hard. Keep the states *aligned*: the animation is only
impressive when most tokens survive the edit, so don't reformat, rename, or re-indent between
states unless that IS the change.

```bash
mkdir -p "$WORK/states" && cd "$WORK/states"
cat > before.java <<'EOF'
@RestController
@RequestMapping("/api/v1/users")
class UserController {

    @GetMapping
    List<User> findAll() {
        return service.findAll();
    }
}
EOF
```

Print the states and intended block, then build and snapshot before rendering. Set WORK to the
project folder above. Keep the generated project for revisions; do not reinstall or retokenize
unchanged states. A changed source state invalidates tokens and the downstream render.

## Step 2 — Tokenize

The blocks do NOT take plain text. Each token is a keyed span, and **a token that keeps its key
across states is what glides** — so the key assignment IS the diff. `tokenize.mjs` runs Shiki over
each state and chains an LCS between consecutive states to assign the keys.

```bash
node <skill>/scripts/tokenize.mjs \
  --seq diff --lang java --theme vitesse-dark \
  --out tokens.json before.java after.java
```

`--seq` must match the block (see the table). `--lang` is any Shiki id (`java`, `kotlin`, `xml`,
`properties`, `bash`, `json`). It prints the carry count:

```
diff: 44 tokens → 53 tokens · carried (glide): 43
```

**Read that number.** A high carry count means a tight, readable animation. If carry is low
relative to the token count, the two states drifted apart — usually reformatting — and the whole
snippet will re-type instead of the one line moving. Fix the fixtures and re-run.

## Step 3 — Build and render

`build.mjs` applies the brand swaps, sizes the editor card to the snippet, and splices the tokens in.

```bash
node <skill>/scripts/build.mjs \
  --block <skill>/assets/blocks/code-diff.html \
  --tokens tokens.json --out proj/index.html --filename UserController.java

printf '{"name":"%s","width":1920,"height":1080,"fps":30}\n' "$NAME" > proj/hyperframes.json
```

The renderer wants `index.html` at the **project root** plus a `hyperframes.json` — it will not
find a composition anywhere else. Snapshot the start, change, and settled state and inspect them
before encoding. Render the MP4 insert by default. Run the alpha command only when an overlay
is needed; an additional format is not a mandatory second deliverable:

```bash
# the insert itself
cd proj && npx -y hyperframes@0.7.77 render . \
  --output renders/$NAME.mp4 --fps 30 --quality high --gpu

# OPTIONAL transparent overlay, only when the edit needs it
node <skill>/scripts/build.mjs --block <skill>/assets/blocks/code-diff.html \
  --tokens ../tokens.json --out ../alpha/index.html --filename UserController.java --transparent
cp hyperframes.json ../alpha/
cd ../alpha && npx -y hyperframes@0.7.77 render . \
  --output renders/$NAME-overlay.webm --format webm --fps 30 --quality high
```

Match `--fps` to the video's real frame rate (`ffprobe … r_frame_rate`). Rendering is fast —
~7.5s for a 6s 1080p clip on the M4 Max. For 4K use `--resolution landscape-4k`.

If `build.mjs` warns that brand swaps did not match, upstream block CSS changed. Fix the swap
list rather than hand-editing the vendored block.

## Step 4 — Verify, then deliver

- `npx hyperframes@0.7.77 snapshot . --at <t1>,<t2> --no-end --output snaps` and **look at the
  contact sheet.** Check: nothing clipped off the right edge, the final state is the correct code,
  the card isn't a thin strip.
- Composite a short preview with surrounding narration using the shared graphics plan and
  `video-motion-graphics/scripts/composite.py`. Check that the actual change, rather than the
  animation start, aligns with its spoken explanation. Adjust the block timeline to the
  narration; do not force every explanation into an identical stock duration.
- Confirm the animation actually settles before the clip ends. `code-diff` finishes around 3.6s of
  its 6s — the tail is a static hold, which is a fine handle for the editor but shouldn't surprise you.
- Deliver the requested format: MP4 into `01_Footage/`; an optional alpha master into
  `03_Graphics/overlays/`. For Premiere, prefer ProRes 4444 converted from VP9 using the forced
  libvpx decoder and verify transparency. Use the working-folder fallback above without a project.
- Report: block used, states, carry count, where the files landed.

## Compositing the overlay

The WebM carries VP9 alpha, but ffmpeg picks its **native** vp9 decoder by default and that
decoder silently drops the alpha plane — you get an opaque black box, no warning. Force the
libvpx decoder with `-c:v libvpx-vp9` **before** the overlay input:

```bash
ffmpeg -y -i footage.mp4 -c:v libvpx-vp9 -i overlay.webm \
  -filter_complex "[1:v]setpts=PTS-STARTPTS+12.0/TB[o];[0:v][o]overlay=eof_action=pass[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a copy out.mp4
```

`-c:v` is position-sensitive: it applies to the input that follows it. Putting it after the input
(or omitting it) gets you the black box.

Verify before delivering — composite over magenta and read the corner pixel:

```bash
ffmpeg -v error -y -f lavfi -i color=c=magenta:s=1920x1080 -c:v libvpx-vp9 -i overlay.webm \
  -filter_complex "[0:v][1:v]overlay=shortest=1" -ss 3.6 -frames:v 1 /tmp/proof.png
ffmpeg -v error -i /tmp/proof.png -vf "crop=8:8:0:0,scale=1:1" -f rawvideo -pix_fmt rgb24 - | xxd -p
```

`fd00fc`-ish (magenta) means alpha decoded. `000000` means it didn't.

## Pitfalls log

Append a dated line when a run burns you.

- (2026-07-28) The blocks are **pre-tokenized**; there is no "paste your code here" and no
  `--variables` hook. `window.__TOKENS` is baked into the HTML and must be rewritten. That's the
  whole reason `tokenize.mjs` exists.
- (2026-07-28) Token **keys are the diff**. Matching keys glide; fresh keys read as added. Naive
  per-state keys make every token re-render and the effect dies.
- (2026-07-28) The stock blocks hardcode a **1380×800 editor regardless of content** — an 8-line
  snippet leaves half the card empty. `build.mjs` sizes it from line count and longest line.
- (2026-07-28) Width math must budget the **diff chrome** (22px sign + 14px indent) on top of the
  104px gutter and 44px padding. Forgot it on the first pass and the longest changed line clipped
  off the right edge.
- (2026-07-28) VP9 alpha: ffprobe reports `pix_fmt=yuv420p` and only the `ALPHA_MODE: 1` tag hints
  at it. ffmpeg's **native** vp9 decoder drops the alpha plane silently — the composite comes out
  a solid black box with no warning. The fix is `-c:v libvpx-vp9` before the overlay input, and
  `-c:v` is position-sensitive. A `format=yuva420p` in the filter graph looks like it fixes this
  and does nothing; I chased that wrong fix for two rounds. Always run the magenta proof above.
- (2026-07-28) `code-morph` on a **single long line** renders a thin 1380×174 strip that looks
  broken. Morph wants multi-line states; for a one-liner use `code-diff`.
- (2026-07-28) `snapshot` takes a project DIR, not `--composition <file>` (the docs list a flag
  that doesn't exist at 0.7.77). Docs drift — trust `--help` over the website.
- (2026-07-28) Upstream ships a `<!-- hyperframes-registry-item -->` comment **before** the
  doctype, which trips their own StaticGuard. `build.mjs` strips it.
- (2026-07-28) Blocks load GSAP from a jsDelivr CDN at render time — an otherwise-local pipeline
  needs network. If a render fails offline, that's why. Vendor GSAP if it becomes a problem.
- (2026-07-28) HyperFrames is pre-1.0 (0.7.77). The composition contract (`data-composition-id`,
  `data-start`, `window.__timelines`) will move. The version is pinned deliberately — re-verify
  every block before bumping it.

## What this skill does NOT do

- Graphics over existing footage — cards, lower thirds, callouts, spotlights, zooms
  (`video-motion-graphics`).
- Cutting, pacing, filler removal (`video-rough-cut`).
- Captions, vertical clips (`video-shorts`), thumbnails (`video-packaging`).
- Do NOT run `npx skills add heygen-com/hyperframes`. It installs 19 skills including one named
  `motion-graphics` that collides with this repo's naming convention. Use the pinned CLI and the
  vendored blocks.
