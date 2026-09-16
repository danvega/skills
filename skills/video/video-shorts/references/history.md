# Historical shorts incidents

Evidence only; current instructions supersede old workarounds, including integer frame rates.

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
- 2026-07-28: **a static crop cannot follow a scrolling IDE.** Two-band (code / terminal) crops
  verified fine on a mid-clip frame and still broke elsewhere in the same clip: in one clip Dan
  switched the bottom panel from the Run/Console tab to the Terminal tab, so the band landed on
  IntelliJ's status bar; in another the editor was still scrolled to a previous method when the
  clip started, so the top band opened on unrelated code. Sample the OUTPUT at >=3 points spread
  across the clip (not just the middle) before shipping. When content drifts, fall back to ONE
  band covering the whole editor+panel (`crop=1440:1020:480:55` on 1080p, which drops the project
  tree) — everything stays in frame at ~0.75x, at the cost of smaller text.
- 2026-07-28: **wide payoff text caps the magnification.** Console lines like "Secret found in
  model response, replacing it before it reaches the caller" span most of a 1920px frame, so any
  crop containing them scales ~1.0-1.5x at 1080 wide. That caps content at roughly 500-1000px in a
  1920-tall frame, i.e. large black bands are unavoidable for dense IDE screen-share. Put the
  content above the caption band and treat the black as intentional; do not crop tighter and
  truncate the payoff line.
- 2026-07-28: on this project the camera bubble existed ONLY over the browser segments, never over
  the full-screen IDE, so the stacked cam layout was impossible for every candidate clip. Check for
  the bubble before planning the reframe, not after picking clips — it changes the whole layout.
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

- 2026-07-30: render.mjs parses `--fps` as an INTEGER — `--fps 29.97` renders caption frames
  timed at 29 fps. Feeding them to ffmpeg at `-framerate 30000/1001` makes the word-pop drift
  ~3% fast (about 1s by the end of a 30s clip; too small to catch on spot frames, real on
  watch-through). Feed the caption PNG input at `-framerate 29` — overlay syncs by timestamp,
  mixed rates are fine. Or render at a whole-number fps and match.
- 2026-07-25: 3 sampled frames per clip is NOT enough to classify mode — Dan's final edits
  contain full-screen b-roll inserts (Premiere-built explainer graphics) inside talking-head
  sections, and one landed between my samples: the face crop shipped a mangled slice of a yaml
  graphic. Always scene-detect the clip span (`select='gt(scene,0.25)',showinfo`) and check one
  frame per shot. If an insert is 16:9 graphics: split the reframe at the hard cuts — face crop
  for cam shots, `scale=1080:608,pad=1080:1920:0:656` letterbox for the insert; the caption band
  at bottom:560 clears the letterboxed area with ~20px to spare. Watch for the insert's own
  baked-in caption line stacking above ours — acceptable, but don't add a hook card on top too.
