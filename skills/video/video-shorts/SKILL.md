---
name: video-shorts
description: >-
  Chop a long-form video into 30–60 second 9:16 vertical shorts — find the standalone moments in
  the transcript, reframe per segment (face crop for talking-head, stacked layout for
  screen-share), burn in word-by-word "karaoke pop" captions, and render a house-style thumbnail
  for each YouTube-bound short (two approved themes, varied across the batch). Runs on the FINAL
  export in the project's 04_Exports folder, after Dan's final edit. Use when
  Dan says "make some shorts", "chop this up", "pull some clips out of this", "clip this video",
  "vertical clips", "9:16", or mentions Shorts / Reels / TikTok for an existing video — and also
  for shorts thumbnail work on its own ("redo this short's thumbnail", "thumbnails for the
  batch"). Do NOT use for the long-form first pass (video-rough-cut), graphics on the long-form
  video (video-motion-graphics), or the long-form video's title/thumbnail (video-packaging).
---

# Shorts

Pull the **2 to 3** strongest moments from a long-form video that genuinely stand alone, and
deliver each as a finished 1080×1920 short with word-level captions. Three is the ceiling (Dan,
2026-09-28: "I'm creating too many shorts"). At one a day in the noon queue, a bigger batch
crowds out the next video's shorts. List the runners-up under "Skipped" so Dan can swap one in.
Also avoid two shorts that make the same point. Quality bar over quota: a video with one great
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
- Transcribe the exact final export, reusing a cached transcript only when its source identity
  and ASR settings match. Use `video-rough-cut/scripts/pipeline.py transcribe <final.mp4>
  --work <project>/05_Transcripts/final`. Read the transcript path from `transcripts.json`.
  This extracts audio directly and skips silence analysis. Earlier rough-cut transcripts are
  on a different clock and must not supply final-export timestamps.
- Optional: explicit asks ("clip the part about virtual threads") — these skip ranking.

Working dir: `<project>/03_Graphics/shorts/<basename>/`; set `$WORK` to this path.
Keep captions and editable plans here, with rendered frames under `cache/`. Without a project,
use `<source_dir>/shorts/<basename>/`. Final delivery is in Step 6.

## ⚠️ Clock mapping (same trap as video-motion-graphics)

**Standard flow (final export, transcribed fresh): there is no mapping.** The transcript was made
from the very file being cut, so transcript time == video time — run `scripts/extract_words.py`
WITHOUT `--filter` (mapping is identity) and use timestamps directly.

For an explicitly agreed rough-cut fallback, prefer that edit's `transcript.output.json` and
use output-clock clip windows with no `--filter`. It already accounts for multiple sources and
speed changes. If its words need boundary review, listen or transcribe the delivered cut.

The legacy `--filter` option supports only an old single-source, cuts-only `filter.txt` with a
source-clock transcript. It cannot represent multiple source clocks or speed changes. Use a
verified mapped transcript for those cases instead of trying to reconstruct their timing here.

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

Scene-detect each clip span and inspect at least one frame per shot, plus the start/end, to classify its footage
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
# TRANSCRIPT is the exact export transcript path from transcripts.json.
# 1. words for the clip, clip-relative — also prints OUT_A/OUT_B for ffmpeg
#    (standard flow: fresh transcript of the final export, same clock, NO --filter;
#     mapped rough-cut transcript: also no --filter; see legacy limitations above)
python3 <skill>/scripts/extract_words.py \
  --json "$TRANSCRIPT" --start 42.3 --end 78.1 \
  --out $WORK/clip1_words.json

# 2. Write clip1_params.json with style="danvega" and words=the parsed words array.
# Render only this clip, preserving the actual sequence frame rate.
node <video-motion-graphics>/scripts/render.mjs \
  --template <skill>/assets/captions.html \
  --params-file "$WORK/clip1_params.json" \
  --duration <clip len> --fps 30 --width 1080 --height 1920 \
  --out $WORK/clip1_cap
```

Use a short caption-dense preview first. Reuse renderer cache when parameters are unchanged.
Long caption sequences still require many browser captures; measure their cost before increasing
concurrency. Never run two renderers against the same frame directory.

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
# SRC is the final export (or an explicitly agreed intermediate).
ffmpeg -nostdin -y -hwaccel videotoolbox -ss $OUT_A -to $OUT_B -i "$SRC" \
  -framerate 30 -i $WORK/clip1_cap/f_%04d.png \
  -filter_complex "[0:v]crop=1214:2160:$X:0,scale=1080:1920[v];\
[v][1:v]overlay=0:0:eof_action=pass[out]" \
  -map "[out]" -map 0:a -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v h264_videotoolbox -b:v 12M -pix_fmt yuv420p -c:a aac -b:a 192k \
  $WORK/short1.mp4
```

(Screen-share clips: build `[v]` with the Step 2 stack instead of the crop.) Match the caption
`--fps` to the source's frame rate if it isn't 30. Verify each short before delivering: extract
a frame mid-clip and at the hook — captions on, correctly styled, framing right, nothing
clipped — and confirm duration fits the selected moment (normally 30 to 60 s; do not pad a strong shorter clip).

## Step 6 — Deliver

- Deliver to `<project>/04_Exports/shorts/<name>_short1_<slug>.mp4`; without a project, use
  `<source_dir>/shorts/`. Derive the slug from the hook, then open the folder.
- Report per clip: timestamps (orig → out), duration, mode, caption style, suggested Shorts
  title, and the skipped candidates with reasons.
- Keep the editable captions and framing plan; revisions reuse analysis and unchanged renders.

## Step 7 — Thumbnails (YouTube-bound shorts only)

Every short headed for YouTube gets a custom thumbnail; X clips don't (the board posts them
with a tweet, no thumbnail). Never leave the app's auto-generated thumbnails in place — Dan
has rejected both built-in generator styles every time (2026-07-30 ×2).

**Two approved themes, and vary them across the batch (Dan, 2026-07-31: "mix up the
styles").** A batch where every thumbnail is the same theme looks like wallpaper on the
channel's Shorts shelf; alternate dark/light (or roughly half/half for larger batches) so
adjacent shorts read as distinct videos. Templates are bundled here:

- `assets/thumb-house-dark.html` — dark green gradient + dot grid, Komika Axis title at
  -2deg, green underline rule (Komika Axis: `~/Library/Fonts/KOMIKAX_.ttf`).
- `assets/thumb-light.html` — cream + green top bar, heavy black Helvetica 900 title.

Both take `{{KICKER}}` (short mono setup line, e.g. "IT WORKS ON YOUR MACHINE"),
`{{TITLE_HTML}}` (3-ish short lines via `<br>`, exactly one `<span class="accent">` word —
the payoff word; use curly apostrophes, straight ones look cheap at 148px), and
`{{CUTOUT_PATH}}`.

**Match the cutout's emotion to the clip's message** — this matters as much as the theme.
Dan rejected a grimace on a "this works, BUT…" short; point-surprised fit. Cutout library
(real photo PNGs labeled by expression) lives in
`/Users/vega/youtube/shared-assets/thumbnail/cutouts/`; copy the ones you use into this
project's `06_Thumbnails/` so each project folder stays self-contained.

Render into the project's `06_Thumbnails/shorts/` (keep the filled .html next to the .png
for fast revisions):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --window-size=1080,1920 --hide-scrollbars --screenshot=<name>.png "file://$PWD/<name>.html"
sips -s format jpeg -s formatOptions 85 <name>.png --out <name>.jpg   # stays well under YouTube's 2MB
```

Show Dan the renders (SendUserFile) and get a pick/OK **before** loading anything into
ContentOS — he has strong opinions here and a swap after upload means re-pushing to YouTube.
To load an approved thumbnail, overwrite the fixed-name file
`~/contentos-files/projects/<slug>/videos/thumbnails/short-thumb-<videoId>.jpg` (asset row
persists; the board's Replace thumbnail button is the alternative). Whatever file sits there
when the draft uploads is exactly what YouTube gets.

## Step 8 — Schedule and link the related video (YouTube-bound shorts)

Runs after the drafts are on YouTube (the board's upload). Dan's rule (2026-09-28): **one
short a day at noon Eastern, channel-wide, and a new video's shorts go ahead of older queued
ones.** Every batch also gets its long video as each short's Related video. Dan asked for both
on every batch, so do them without being asked again.

1. **Schedule.** Open `/projects/<slug>/videos/shorts/schedule` in ContentOS. It reads the real
   queue from YouTube and shows the plan without changing anything. Shorts from newer long
   videos keep their days. Use a draft's **Leave out** link for any short Dan dropped (it stays
   private and the choice carries into Apply). Show Dan the dates, and
   apply only after he says go, because it sets public publish times. From Claude in Chrome,
   submit the Apply form with `fetch(form.action, {method: 'POST', body: new URLSearchParams(new
   FormData(form))})`: a ref click on the button did nothing. Reload the preview afterwards.
   Every row should read "No change", which proves YouTube stored the times.
2. **Related video.** The YouTube API has no field for it, so set it in Studio through Dan's
   logged-in Chrome, one short at a time, at `https://studio.youtube.com/video/<id>/edit`:
   - Find the "Related video" button and click it. The first click after a page load often
     does nothing. Click again, then wait about 8 seconds for the "Choose specific video" picker.
   - Find the long video's tile by its full title. Wait until the tiles have thumbnails before
     clicking it. A click while they are still gray does not register.
   - A good click usually closes the picker and fills the field. If the picker stays open with
     the tile highlighted, close it with its X. Never press Escape, because that dropped the
     choice once. Then find Save in the page header fresh each time (its ref changes) and click it.
   - Reload the page and confirm the Related video field shows the long video's title.
3. Reload the schedule preview once more. Saving in Studio should leave every publish time as
   is ("No change").
4. **Thumbnails, after processing.** The thumbnail set during upload is often lost when YouTube
   finishes processing (2026-09-28: the Model Router and Claude Code shorts all fell back to
   auto frames). In Studio, a processed short that shows a video frame in the Thumbnail box has
   lost it; the "…" placeholder is fine. POST the board's `/{videoId}/youtube-thumbnail` for
   each lost one (50 units), then fetch the signed `i9.ytimg.com` URL from the "Thumbnail
   confirmed" log line and look at it. That shows what YouTube stored. The public
   `i.ytimg.com` URL is a gray placeholder for private drafts, so it proves nothing.

## Operational checks

- Preserve the actual decimal or rational frame rate throughout caption capture and encoding.
  The shared renderer supports `30000/1001`; the old integer-rate workaround is obsolete.
- Inspect one frame per detected shot, including full-screen B-roll inserts. Split framing at
  mode changes. A face crop over an explainer graphic can destroy its meaning.
- Confirm the camera region really contains Dan throughout a stacked clip. If it disappears,
  choose another layout. Inspect scrolling code and changing terminal tabs across the whole clip.
- Keep caption word spacing sufficient at the largest animated scale; transformed glyphs can
  collide even when their unscaled layout fits. Do not duplicate an insert's baked-in captions.
- Bound looped still inputs and set overlay EOF behavior so the render ends with the clip.
- Require even crop dimensions. Do not assume drawtext/libass exists: check before using it.
- The final export carries the video-motion-graphics overlays. Before choosing a face-crop x or a
  stacked top box, check which cards fall inside the clip span (lower-third, chapter titles sit
  bottom-left and reach x≈690 at 1080p): a card edge in the crop or a chapter card under the
  captions is a re-render (ColdFusion, 2026-09-15: both happened, fixed by x=730 and a top box
  cropped above the card).
- Wait for the caption renderer PROCESS to exit before cutting the short. Polling for
  `render.json` fired early once and the short went out with captions that stopped partway.
- Run short clip previews before batch delivery. Full-output sampling must include start, end,
  mode changes, and payoff text, not just the midpoint.
- Resolve shared photo cutouts from `/Users/vega/youtube/shared-assets/thumbnail/cutouts/`,
  following video-thumbnail's library. Do not rely on another project's private asset copies.
- Historical evidence is in [history.md](references/history.md). Update current rules after a
  lesson rather than appending contradictory instructions.

## What this skill does NOT do

- Long-form cutting or pacing — that's video-rough-cut, run it first.
- Branded overlay graphics on shorts (lower thirds, callouts) — video-motion-graphics, if ever needed.
- Titles, descriptions, hashtags strategy, and the LONG-FORM video's thumbnail —
  video-packaging territory. (Shorts thumbnails ARE this skill's job — Step 7.)
- Uploading anywhere other than the ContentOS shorts board, or scheduling outside the noon queue
  in Step 8.
