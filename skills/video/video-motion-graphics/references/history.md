# Historical graphics incidents

Evidence only. Follow the current SKILL.md and rendering.md when old advice conflicts.

## Pitfalls log

Append a dated line when a run burns you.

- (seed) `backdrop-filter` does not render in headless capture — rely on the card's own bg alpha.
- (seed) Alpha survives only in ProRes 4444 (`yuva444p10le`) or VP9/webm — libx264 `yuv420p`
  silently drops it. The composite is x264; the *overlay masters* must be ProRes.
- (seed) Install playwright with `PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1` and launch
  `channel: "chrome"` — the npm postinstall browser download is slow and unnecessary.
- (seed) During the typing phase the whoami card already reserves the answer's space (brief
  tall-card look). Acceptable; animate card height if it ever bothers us.
- (seed) Overlay frames must match the video's pixel dimensions — a 1080p overlay on a 4K video
  composites quarter-size in the top-left corner. Render at the right size with `--scale`; don't
  upscale the PNGs in the ffmpeg graph (blurry text).
- (2026-07-16) Don't default the lower-third to the cold-open hook. Dan often introduces himself
  by name a bit later ("My name is Dan Vega…"); the card lands far better there. Grep the
  transcript for the self-intro before placing — see Step 1's priority order.
- (2026-07-16) Sync is to the REVEAL, not the card start. The whoami card types first, so the name
  isn't up until ~1.8s in. Placing render_start at the spoken name made the name appear ~2s late.
  Set render_start = (word-level timestamp of the name) − REVEAL_OFFSET, then verify with a frame
  at the reveal moment. See Step 1's reveal-offset table.
- (2026-07-16) BIGGEST one: `audio.json` is on the ORIGINAL recording clock; the rough cut you
  composite onto is TRIMMED. Used transcript time directly → card fired ~5s late (dead air before
  the intro had been cut). Always map original→output via `filter.txt` before placing. See the ⚠️
  block at the top of Step 1. This compounds with the reveal offset — get both right.
- (2026-07-16) Dan's videos are NOT all talking-head — they cut to screen-share with a white page
  and a bottom-right camera bubble. First section-title draft (white text, no panel) vanished on
  the white page; first subscribe-nudge (bottom-right) covered his face. Fixed both. Preview every
  new template over a real screen-share frame, not just the cam shot. See the screen-share note.
- (2026-07-16) `zoompan` defaults its output size to 1280×720 — omit `s=WxH` and the zoomed
  segment silently downscales (then the concat fails on mismatched sizes, or worse, succeeds
  scaled). Always set `s=` to the video's native size, and `fps=` to its real frame rate.
- (2026-07-16) Code screen-share IS in scope after all (the 02 coding walkthroughs). Use
  `spotlight` / code zoom-to-region on the beats that matter — error responses, the key method, the
  one-line switch — not every line. Measure the region as fractions on a real extracted frame;
  `spotlight` and the zoom crop both take the same fractional box.
- (2026-07-16) The lower-third is once per SERIES, not per video. 02 (a continuation) got a "who I
  am" card it shouldn't have — the viewer already met Dan in 01. In a set, only the FIRST video
  gets the lower-third; continuation videos (numbered `_02+`, or no self-intro after a series
  opener) skip it. See step 0 of the lower-third rule.
- (2026-07-23) "Deliver to the launch cwd" misfires when the skill is invoked from a code repo
  (e.g. the ContentOS session): the artifacts would land in the repo. When the video has a
  scaffolded project under `/Users/vega/youtube/<Project>/`, deliver there instead — composite
  into `01_Footage/`, ProRes overlays into `03_Graphics/overlays/`. The cwd rule is only the
  fallback for videos with no project folder.
- (2026-07-28) `to_out` must SNAP, not reject. Whisper word times carry ±100–300ms of error, so an
  anchor word routinely lands just inside a removed region even though the word itself survived
  (the trim boundary sits mid-word). A strict `return None` rejected the first spoken word of 6 of
  7 parts and looked like a broken trim map. Verify against the delivered audio before believing
  it — the words were all there. Snap an out-of-keep timestamp to the nearest surviving keep edge.
- (2026-07-28) On Dan's IntelliJ coding videos the **terminal/Build Output panel spans the FULL
  bottom** of the frame during demo runs, so bottom-left AND bottom-right both cover the payoff
  output — `side:"right"` does not save you. The fix is temporal, not positional: shift the card a
  few seconds to a moment when the panel is closed (a chapter marker does not need frame-exact
  sync). Also watch for IntelliJ **autocomplete popups**, which cover the lower-middle-left.
  Extract candidate frames a few seconds either side and pick the calm one.
- (2026-07-28) This ffmpeg build has no `drawtext` filter (compiled without freetype), so labelled
  contact sheets fail with "No such filter". Extract plain frames in a known order instead.
- (2026-07-28) Classified a clip as talking-head from two spot frames; it switched to
  screen-share at 2:11 and both planned punch-ins landed on a browser page (caught in verify,
  re-composited without zooms). Run the contact-sheet sample (`fps=1/20,tile=4x4`) over the WHOLE
  clip before planning any zoom — the mode can change mid-clip, and every zoom segment must be
  checked against the frames it actually covers, not the clip's opening.
- (2026-07-23) A multi-part recording (video-rough-cut of `_01..\_05` parts concatenated) has per-part
  trim maps: `t_out = to_out_part(t) + sum(prior parts' rough durations)`. Build the combined map
  before placing anything; the seams themselves are the natural chapter boundaries for
  section-titles.
- (2026-09-15, ColdFusion) Two cheap wins. (1) When the inputs are the delivered rough cuts (or any
  already-trimmed file), re-transcribe THEM (mlx_whisper, ~20s per 10 min) instead of mapping the
  rough cut's original-clock `audio.json` through `filter.txt`: the transcript then shares the
  composite's clock, and the whole reveal-offset/trim-map error class goes away. (2) The scope-gate
  contact sheet `fps=1/20,tile=4x4` only covers the first 320s. An 11-min clip looked all
  screen-share until a second sheet from `-ss 300` showed the on-camera outro. Use
  `fps=1/(duration/16)` so the 16 tiles span the whole clip.
