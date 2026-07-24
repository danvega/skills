---
name: video-shorts
description: >-
  Chop a long-form video into 30–60 second 9:16 vertical shorts — find the standalone moments in
  the transcript, reframe per segment (face crop for talking-head, stacked layout for
  screen-share), and burn in word-by-word "karaoke pop" captions. Runs on the FINAL export in the
  project's 04_Exports folder, after Dan's final edit. Use when
  Dan says "make some shorts", "chop this up", "pull some clips out of this", "clip this video",
  "vertical clips", "9:16", or mentions Shorts / Reels / TikTok for an existing video. Do NOT use
  for the long-form first pass (video-rough-cut), graphics on the long-form video (video-motion-graphics), or
  titles/thumbnails (video-packaging).
---

# Shorts

Pull the 3–5 moments from a long-form video that genuinely stand alone, and deliver each as a
finished 1080×1920 short with word-level captions. Quality bar over quota: a video with one great
clip yields one; a video with nothing clippable yields zero and a report saying why. A mediocre
short costs channel credibility — **when in doubt, leave it out** (the inverse of video-rough-cut's
rule, on purpose: video-rough-cut keeps, shorts curates).

## Inputs

- **The video — the FINAL export, not an intermediate (Dan, 2026-07-23).** Source clips from the
  finished edit in the project's `04_Exports/` folder (`/Users/vega/youtube/<Project>/04_Exports/`)
  whenever it exists — that's the artifact with Dan's final pacing, graphics, and fixes, and it's
  what published shorts must match. Rough cuts and `_gfx` composites are intermediates: Dan's
  Premiere pass changes timing after them, so clips cut from those won't line up with the
  published video. If `04_Exports/` is empty, say so and ask whether to proceed from the latest
  intermediate instead — don't silently fall back.
- The final export has no transcript on the same clock — transcribe it first (video-rough-cut Step 2:
  proxy + `mlx_whisper`) into `/tmp/shorts/<basename>/`. One clock, no trim mapping needed. Any
  transcript from an earlier video-rough-cut run is on a DIFFERENT clock (the final edit re-times
  everything) — never reuse it for clip timestamps.
- Optional: explicit asks ("clip the part about virtual threads") — these skip ranking.

Working dir: `/tmp/shorts/<basename>/`. Final shorts are copied out (Step 6).

## ⚠️ Clock mapping (same trap as video-motion-graphics)

**Standard flow (final export, transcribed fresh): there is no mapping.** The transcript was made
from the very file being cut, so transcript time == video time — run `scripts/extract_words.py`
WITHOUT `--filter` (mapping is identity) and use timestamps directly.

The trap only exists in the fallback flow (cutting an intermediate rough cut with a reused
transcript): `audio.json` is then timestamped on the **original recording** while the rough cut
is **trimmed**, and every transcript time — clip boundaries AND caption words — must map through
the trim before touching the video. In that case give `extract_words.py` the clip window on the
transcript's clock plus the rough cut's `filter.txt`; it prints the mapped `-ss/-to` boundaries
and writes clip-relative caption words. Work in transcript times everywhere in Step 1; only
convert at the extract step. Rule of thumb: `--filter` if and only if the transcript and the
video are on different clocks.

## Step 1 — Find the clips (transcript first, ranked)

Read the whole transcript and hunt for moments that survive being ripped out of context:

- **Self-contained** — no "as I showed earlier", no dangling "this" pointing at something
  off-screen, no dependence on the demo state. If the first sentence needs a setup, it fails.
- **Hooks in the first ~2 seconds** — a question, a bold claim, a number, "the biggest mistake
  people make with X". The hook is the clip's first spoken words; viewers decide in one swipe.
- **One idea, with a payoff** — the clip ends on a resolution beat (the answer, the punchline,
  the "and that's why…"), not mid-thought. 30–60s target; a killer 25s beats a padded 60s.
- Strong candidates in Dan's material: hot takes and opinions, "the one thing" tips,
  myth-busting, before/after or wrong-way/right-way, a demo moment with a visible aha, list
  items that stand alone ("tip 3 of 5" works if the tip itself is complete).

**Boundaries:** start at the hook's first word onset − 0.15s; end at the payoff's last word
+ 0.3s. Snap to word timestamps, never to segment starts (segments begin with breaths). Keep the
span contiguous — no internal re-editing in v1; the rough cut already tightened it.

Print the plan, then render in the same turn (render-first contract — revisions are cheap):

```
CLIP 1  ★★★  0:42–1:18 orig → 0:37–1:13 out  (36s, talking-head)
  Hook: "Stop writing retry logic yourself."
  Payoff: built-in @Retryable demo lands
  Suggested title: Spring Boot 4 killed my retry boilerplate
CLIP 2  ★★   …
Skipped: 6:10 virtual-threads riff — references the earlier benchmark, not standalone.
```

## Step 2 — Reframe plan, per clip

Classify each clip's footage by extracting 3 frames across it and **looking at them**
(talking-head vs screen-share vs mixed — same check as video-motion-graphics). Avoid clips that cut
between modes in v1; if a great clip mixes, split the reframe at the mode change.

**Talking-head → face crop.** Crop a 9:16 window at full height, centered on the face. Read the
face position off the extracted frame and set the x offset (fractional, like spotlight boxes).
Static crop per clip — no tracking in v1; Dan sits fairly still.

```bash
# 4K source: 9:16 at full height = 1214x2160 (MUST be even — 1215 breaks x264)
CROP_W=1214; X=<face_center_px - CROP_W/2, clamped to [0, iw-CROP_W]>
```

**Screen-share → stacked layout.** Full-frame screen scaled into 1080 wide is unreadable on a
phone. Instead: top = the code/content region that matters (measure a fractional box off a real
frame, exactly like a spotlight), bottom = the camera bubble. Screen gets ~60–65% of the height:

```bash
ffmpeg ... -filter_complex "\
[0:v]crop=CW:CH:CX:CY,scale=1080:-2[top];\
[0:v]crop=BW:BH:BX:BY,scale=1080:-2[cam];\
[top][cam]vstack,crop=1080:1920:0:0,setsar=1[v]" ...
```

Heights won't sum to 1920 exactly — widen one crop box (keep aspect, more context) until they do,
or pad the seam with black. Verify: extract one frame of the OUTPUT and confirm the code is
legible at phone size and the camera bubble isn't clipping Dan's head.

## Step 3 — Captions (word-by-word pop)

Every short gets burned-in captions — most Shorts viewers watch muted, and the word-follow style
is the current standard (Hormozi-style: 1–3 words visible, heavy sans, active word colored with a
scale pop). The local ffmpeg has **no libass/drawtext**, so captions render as a transparent PNG
sequence from `assets/captions.html` via the video-motion-graphics renderer (this skill depends on
`../video-motion-graphics/scripts/` being installed and npm-installed), then composite with `overlay`.

```bash
# 1. words for the clip, clip-relative — also prints OUT_A/OUT_B for ffmpeg
#    (standard flow: fresh transcript of the final export, same clock, NO --filter;
#     add --filter /tmp/rough-cut/$NAME/filter.txt ONLY in the reused-transcript fallback)
python3 <skill>/scripts/extract_words.py \
  --json /tmp/shorts/$NAME/audio.json --start 42.3 --end 78.1 \
  --out /tmp/shorts/$NAME/clip1_words.json

# 2. render caption frames (params JSON inline; words file content goes in "words")
node <video-motion-graphics>/scripts/render.mjs \
  --template <skill>/assets/captions.html \
  --params "{\"style\":\"danvega\",\"words\":$(cat /tmp/shorts/$NAME/clip1_words.json)}" \
  --duration <clip len> --fps 30 --width 1080 --height 1920 \
  --out /tmp/shorts/$NAME/clip1_cap
```

A 60s clip is ~1800 playwright frames ≈ 2–4 min — fine; run clips in the background in parallel.

### Style presets

| Style | Status | Look |
|---|---|---|
| `hormozi` | ✅ approved 2026-07-16 | Montserrat ExtraBold, UPPERCASE, 3 words, green active word + pop |
| `beast` | ✅ approved 2026-07-16 | Impact, UPPERCASE, 4 words, yellow active word + pop |
| `danvega` | ✅ **DEFAULT** 2026-07-16 | Komika Axis, UPPERCASE, 3 words, brand-green active word + pop |
| `clean` | 🧪 candidate | Poppins SemiBold, sentence case, 4 words, soft green active word, no pop |
| `mono` | 🧪 candidate | Menlo Bold, lowercase, 3 words, terminal-green active word — subtle brand nod |

`danvega` is the default ("omg i love that one — it's perfect", 2026-07-16); use it unless Dan
names another style. `hormozi` and `beast` are approved alternates.

**First run / style tryouts:** pick a caption-dense ~8s stretch of a real clip and render it once
per candidate style (`"style":"X"`, or override `font`/`weight`/`fontSize`/`highlight` — any
installed family works: Montserrat, Poppins, Impact, Arial Black, Nexa Bold, Avenir Next…),
`open` all of them, and let Dan pick. Promote the winner to ✅ with a date; it becomes the default.

Captions sit at ~70% height (`bottom: 560` on the 1920 canvas) — clear of the face, above the
Shorts UI zone (bottom ~350px and right edge are covered by title/buttons on the phone).

## Step 4 — Optional hook text

For clips where the spoken hook needs reinforcement, a static text card in the top zone
(y ≈ 200–300) for the first 2.5–3s. No drawtext in this ffmpeg — render it as a single PNG
(an HTML snippet through the same renderer, `--duration 0.04 --fps 25` → one frame) and overlay
with `enable='between(t,0,2.8)'`. ≤ 6 words, and only when it adds information the captions
don't already carry — many strong clips need none.

## Step 5 — Render

One pass per clip: cut, reframe, caption overlay, loudness. `-ss/-to` **before** `-i` so the
clip starts at t=0 (the caption frames are clip-relative):

```bash
ffmpeg -y -hwaccel videotoolbox -ss $OUT_A -to $OUT_B -i "$SRC" \  # SRC = the 04_Exports final (or fallback intermediate)
  -framerate 30 -i /tmp/shorts/$NAME/clip1_cap/f_%04d.png \
  -filter_complex "[0:v]crop=1214:2160:$X:0,scale=1080:1920[v];\
[v][1:v]overlay=0:0:eof_action=pass[out]" \
  -map "[out]" -map 0:a -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v h264_videotoolbox -b:v 12M -pix_fmt yuv420p -c:a aac -b:a 192k \
  /tmp/shorts/$NAME/short1.mp4
```

(Screen-share clips: build `[v]` with the Step 2 stack instead of the crop.) Match the caption
`--fps` to the source's frame rate if it isn't 30. Verify each short before delivering: extract
a frame mid-clip and at the hook — captions on, correctly styled, framing right, nothing
clipped — and confirm duration is 30–60s.

## Step 6 — Deliver

- Copy to the **launch directory**: `<cwd>/shorts/<name>_short1_<slug>.mp4` (slug from the hook,
  e.g. `_short1_stop-writing-retry-logic.mp4`), then `open` the folder.
- Report per clip: timestamps (orig → out), duration, mode, caption style, suggested Shorts
  title, and the skipped candidates with reasons.
- Keep `/tmp/shorts/<name>/` — "use the beast style instead" or "shift the crop left" is a
  seconds-fast re-render.

## Pitfalls log

Append a dated line every time a run burns you.

- (seed) 9:16 crop at 2160p is 1215px wide — odd widths break x264/videotoolbox. Use 1214.
- (seed) `-ss` **after** `-i` keeps original timestamps and every caption lands late. Put
  `-ss/-to` before `-i`.
- (seed) whisper CLI isn't installed here — `mlx_whisper --model
  mlx-community/whisper-small.en-mlx --word-timestamps True` (same JSON shape).
- 2026-07-16: the Homebrew ffmpeg on this machine (8.x, slim formula) has **no libass, no
  drawtext, no freetype** — `subtitles=`/`.ass` burn-in is impossible. That's why captions are
  an HTML template + PNG overlay. Don't re-attempt `.ass` without checking
  `ffmpeg -hide_banner -filters | grep subtitles` first.
- (seed) The transcript is on the original clock, the rough cut is trimmed — run BOTH clip
  boundaries and caption words through `extract_words.py --filter` (see ⚠️ block). Symptom:
  captions drift a few seconds into the clip. (Fallback flow only — the standard final-export
  flow transcribes the export itself, one clock, no `--filter`.)
- 2026-07-23: Dan's rule — shorts come from the FINAL export in `04_Exports/`, never from the
  rough cut or `_gfx` composite. His Premiere pass re-times the video after those, so clips cut
  from intermediates won't match the published long-form. Empty `04_Exports/` → ask, don't
  silently fall back. Always transcribe the export fresh; a reused video-rough-cut transcript is on a
  different clock.
- (seed) Whisper word times are ±100–300ms — pad clip starts 0.15s before the hook word or the
  first syllable gets clipped, which kills the hook.
- 2026-07-16: a hook-card overlay added as `-loop 1 -i card.png` makes the encode run FOREVER
  (the looped image stream never EOFs and the graph keeps producing frames — a 40s clip hit
  1.6GB before being killed). Bound the input with `-t 3` (`-loop 1 -t 3 -i card.png`) and put
  `eof_action=pass` on that overlay.
- 2026-07-23: the camera bubble is NOT on screen for the whole video — in the Tool Calling
  Advisor final edit it disappeared during a deep-coding stretch (full-screen IDE), so a stacked
  short cut there had a blank white cam section (with an autocomplete popup drifting through it).
  Before rendering a stacked clip, extract the CAM CROP REGION (not just full frames) at the
  clip's start/middle/end and confirm the face is in all three. No face for the clip's span →
  drop the clip or use a different layout; don't ship a headless stack.
- 2026-07-23: deliver like video-motion-graphics: when the video has a project folder, shorts go to
  `/Users/vega/youtube/<Project>/04_Exports/shorts/` — the launch-cwd rule is only the fallback
  (launching from a code repo would dump videos into the repo).
- 2026-07-23: zsh does not word-split unquoted variables — `$R --flag` where R="node script.mjs"
  runs a command literally named "node script.mjs" (exit 127), and `set -- $spec` doesn't split
  either. Write multi-command render loops as bash script files and `bash file.sh`, not inline
  compound one-liners.
- 2026-07-16: the active word's scale() pop doesn't reflow layout, so it visually eats the gap
  to its neighbors — words looked glued together ("UNRELIABLELARGE"). Spacing must be margin-based
  and sized per font width (`gap` in the style presets; wide fonts like Komika Axis need ~0.22em
  vs 0.10em), with the big punch coming from the whole-line pulse (`linePop`), which can't collide.
  Check a frame mid-pop on the widest word whenever adding a font.

## What this skill does NOT do

- Long-form cutting or pacing — that's video-rough-cut, run it first.
- Branded overlay graphics on shorts (lower thirds, callouts) — video-motion-graphics, if ever needed.
- Titles, descriptions, hashtags strategy, thumbnails — video-packaging territory.
- Uploading or scheduling anywhere.
