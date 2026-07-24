---
name: video-motion-graphics
description: >-
  Add branded motion graphics and camera moves to a YouTube video — lower thirds, section titles,
  callouts, punch-in zooms — transcript-driven placement, rendered from the terminal-style
  template library and composited with ffmpeg. Chains after video-rough-cut. Use when Dan says "add
  graphics", "add a lower third", "motion graphics pass", "add zooms", "punch in on that",
  "put my name on the intro", or wants callouts / titles / animations / transitions on a video.
  Do NOT use for cutting (video-rough-cut), thumbnails/titles (video-packaging), or captions.
---

# Motion Graphics

Add graphics to a video the way an editor would: decide *what* goes *where* from the transcript,
render each graphic from the branded template library, composite in one pass. Non-destructive —
the source video is never modified, and every graphic also ships as a transparent ProRes `.mov`
for manual work in Premiere.

**Scope gate — talking-head videos only (Dan, 2026-07-16).** This pass is for videos led by Dan
on camera. A video that is predominantly long screen-share doesn't need motion graphics — check
first (contact-sheet sample: `fps=1/20,tile=4x4`) and if it's mostly screen-share, say so and
stop instead of decorating it. On mixed videos (talking-head intro that cuts to screen-share),
graphics anchor to the talking-head moments; the screen-share rules below exist for the moments
where a card must survive those segments, not to add graphics to them.

## Inputs

- The video — ideally a video-rough-cut output, because `/tmp/rough-cut/<name>/` then already has the
  transcript (`audio.json`) and proxy. Without one, transcribe first (see video-rough-cut Step 2).
- Optional: explicit graphics requests ("callout for the repo at 3:10") — these override the plan.

Scratch/working dir: `/tmp/video-motion-graphics/<basename>/` (frames, probes, intermediates).
Final deliverables are copied out to the launch directory — see Step 4.

## Template library

Templates live in `assets/templates/`, all in the site's terminal design language (near-black
green cards, traffic-light chrome, `$`-prompt, SF Mono + system sans, green `#8ce99a` accent).

| Template | Status | What it is |
|---|---|---|
| `lower-third.html` | ✅ approved 2026-07-16 | terminal card: types `$ whoami`, answers name + role |
| `section-title.html` | ✅ approved 2026-07-16 | chapter/topic card: kicker + big title on a backing card |
| `callout.html` | ✅ approved 2026-07-16 | compact chip: accent bar + label + typed URL/repo/version |
| `subscribe-nudge.html` | ✅ approved 2026-07-16 | terminal card: types `$ subscribe`, Subscribe + Like buttons |
| `transition.html` | ✅ approved 2026-07-16 | full-frame branded wipe (stinger) with `$_` mark at a chapter cut |
| `spotlight.html` | ✅ approved 2026-07-16 | dims the frame except a rectangle + green highlight box (code screen-share) |

New templates get approved the way the first one was: render over a real frame of Dan's footage,
show it, iterate, then add to the table with a date.

**Motion moves** (ffmpeg-native, no template):

| Move | Status | What it is |
|---|---|---|
| punch-in zoom | ✅ approved 2026-07-16 | **talking-head:** hard 110% punch on a cut · slow 100→106% push for emphasis |
| code zoom-to-region | ✅ approved 2026-07-16 | **screen-share:** hard or smooth zoom into a code rectangle (fractional target) |
| speed-ramp | ✅ approved 2026-07-16 | **screen-share:** timelapse a long typing/boilerplate stretch (reflows the timeline — see caveat) |

(speed-ramp was briefly dropped as "talking-head only"; it's back in scope now that the skill
handles code screen-share videos like the 02 coding walkthroughs.)

## Step 1 — Direct: build the graphics timeline from the transcript

> **⚠️ CRITICAL — the transcript and the video are on different clocks.** `audio.json` is
> timestamped against the **original recording**, but you composite onto the **trimmed rough cut**
> (`rough_4k.mp4` / `rough.mp4`), which has had dead air and retakes removed. A transcript
> timestamp used directly will land seconds late. **Always map original → output time first.**
>
> The rough cut's trim map is in `filter.txt` (the `trim=start=A:end=B` ranges, kept in order).
> Build the mapping and convert every timestamp before placing a graphic:
>
> ```python
> import re
> keeps=[]
> for a,b in re.findall(r'trim=start=([\d.]+):end=([\d.]+)', open("filter.txt").read()):
>     k=(float(a),float(b))
>     if k not in keeps: keeps.append(k)          # dedupe video/audio duplicate lines
> cum=0.0; maps=[]
> for a,b in keeps: maps.append((a,b,cum-a)); cum+=b-a   # t_out = t_orig + (cum-a)
> def to_out(t):
>     for a,b,sh in maps:
>         if a<=t<=b: return t+sh                 # None => spoken inside a cut; pick another line
>     return None
> ```
>
> Sanity check: `to_out(first_segment_start)` should be ≈ 0–2s (the cut usually trims lead-in
> silence). If a graphic's anchor word maps to `None`, that moment was cut — anchor elsewhere.
> (If there is no rough cut / no `filter.txt`, the transcript and video already share a clock —
> use timestamps directly.)

Read the transcript and propose a plan. Rules per template (only apply rules for templates that
exist):

- **lower-third** — introduces who Dan is, so it belongs **once per SERIES, not once per video**.
  Duration ~6s. Params: `name`, `role` (defaults are Dan's). Never re-show it mid-video.
  **First decide whether this video even gets one:**
  0. **Is this a continuation video in a set?** If so → **no lower-third at all** (the viewer already
     met Dan in the first video). Signals of a continuation: a numbered basename with an earlier
     number present (`…_02`, `_03`, … alongside `…_01`); or an opener that references the series with
     NO self-introduction ("welcome back", "continuing", "in the last video", or just diving into
     "the first thing we're going to do"). The tell is the spoken self-intro: the series opener says
     "My name is Dan Vega"; later parts just start working. No self-intro + continuation signal →
     skip the card entirely, don't fall through to the clean-scene fallback below.
     (This is a series-level call — in a batch, only the FIRST video gets the lower-third.)

  Only if this is the series opener OR a standalone video, place it — **in priority order:**
  1. If Dan says his name/role on camera (grep the transcript for "my name is", "I'm Dan",
     "Dan Vega", "developer advocate"), anchor the card there — it's strongest when the graphic
     confirms what he's saying. **Anchor the name REVEAL to his voice, not the card's first frame.**
     The card types `$ whoami` first, so the name doesn't finish rising until ~1.8s into the
     animation (see the reveal-offset note below). Use the word-level timestamp of the name (the
     `words` array in `audio.json`, not the segment start) and set:
     `render_start = to_out(t_spoken_name) − REVEAL_OFFSET`, where `to_out` maps original→output
     time (see the ⚠️ block above) and REVEAL_OFFSET ≈ 1.8s for lower-third.
     Worked example: transcript says "Dan Vega" at original 40.2s; the rough cut trimmed 5.26s of
     lead-in, so `to_out(40.2) ≈ 34.9s` in the delivered video; minus the 1.8s reveal offset →
     start the card at **33.3s**. Two classic mistakes, both make the name land seconds late:
     (a) using the raw transcript timestamp without mapping through the trim, and
     (b) putting the card's *start* on the spoken moment instead of the *reveal*.
  2. If it's the opener/standalone but has no spoken self-intro, the first clean intro scene is a
     perfectly good home — typically the first full sentence 1.5–3s into speech. Don't force or
     fabricate an intro moment; a clean early scene works. (A *continuation* with no self-intro was
     already excluded in step 0 — this fallback is only for a first/standalone video.)
- **section-title** — at each major topic/section change. Duration ~4s. Params: `num`, `title`
  (or `kicker`), `side`. **Lives in the bottom-left lower-third, same corner as every other card**
  (Dan's preference — never center-screen/mid-frame). Pass `side:"right"` if bottom-left is
  occupied. Has its own backing card, so it reads on dark cam shots AND white screen-share alike.
  Don't overuse — one per real chapter, not every subtopic.
- **callout** — when a URL / repo / version is spoken or shown. Grep the transcript for
  `github.com`, `http`, `spring.io`, `v?\d+\.\d+`, etc.; place at that spoken moment (map through
  the trim). Duration ~5s. Params: `label`, `value`, `side`. Default bottom-left; the value types
  in, so its reveal offset grows with length.
- **subscribe-nudge** — exactly once, at a natural beat 60–75% through. Duration ~6s. Params:
  `channel`, `side`. Default bottom-left (see the screen-share note below).
- **transition** — a full-frame stinger at a chapter cut. Duration ~0.8s. Place it so peak
  coverage (t = total/2) lands ON the seam, i.e. `render_start = cut_time − total/2`. It briefly
  fills the frame opaquely — that opaque moment is what hides the cut. Use sparingly, only at real
  chapter boundaries.
- **punch-in zoom** — **talking-head only**, and only a *blind, center-with-headroom* zoom (the
  thing you must never do over code). Two moves: a **hard punch** (instant 110% exactly on a cut —
  reads as a second camera) when a new point starts, and a **slow push** (100→106% over 3–5s)
  under an emphasis line, snapping back to 100% at the next cut. Cadence: at most every 2nd–3rd
  cut, always returning to 100% between zooms — never stack. Zoom times in the plan are
  **output-clock** times (they describe the delivered video, so no reveal offset — but transcript
  anchors still map through the trim). Plan line:
  `4:12  punch-in 110% (hard)  until 4:19` / `8:03  push 100→106%  over 4s`.
- **spotlight** (code screen-share) — dim the frame except the code being discussed. Best default
  for "look here" on code: keeps the surrounding lines visible, never softens pixels. Params are a
  **fractional** rectangle `x,y,w,h` (0–1) plus optional `label` (e.g. `500 · Bad Request`) and
  `dim`. Measure the box on a real extracted frame. Duration ~4–5s, reveal offset ~0.4s.
- **code zoom-to-region** — the zoom equivalent, for when code is genuinely too small to read
  (see Step 2.5). Aim it at the same fractional center you'd spotlight. Prefer spotlight unless the
  text really needs magnifying. Talking-head punch rules do NOT apply here — this is a deliberate,
  targeted move, not a blind center zoom.
- **speed-ramp** (code screen-share) — timelapse a long typing/boilerplate stretch (Step 2.5).
  Reflows the timeline, so plan it first. Use where nothing is being explained word-by-word.

**Reveal offsets** (seconds from the card's first frame to when the key text is fully on screen;
these come from each template's `seek()` timeline — re-check if a template changes):

| Template | key moment | REVEAL_OFFSET |
|---|---|---|
| `lower-third` | name fully risen | ~1.8s (types `$ whoami` first; role lands ~2.15s) |
| `callout` | value fully typed | ~0.42s + typing (≈ up to ~1.5s; grows with value length) |
| `section-title` | title fully risen | ~0.78s |
| `subscribe-nudge` | buttons up | ~1.9s (types `$ subscribe` first) |
| `transition` | peak cover | total/2 (place render_start = cut − total/2, not − offset) |
| `spotlight` | dim + box up | ~0.4s (label lands ~0.5s) |

When a graphic is meant to sync to spoken audio, subtract its REVEAL_OFFSET from the spoken
timestamp to get the render start.

**Placement is visual, not assumed.** Extract a frame at each insertion time
(`ffmpeg -ss <t> -frames:v 1`) and LOOK at it: default position is bottom-left; if the camera
bubble or important content (code, terminal output) sits there, pass `"side": "right"` or adjust
the time. A graphic that covers what Dan is showing is worse than no graphic.

> **Screen-share segments change the rules.** Dan's videos mix talking-head with screen-share,
> and on the screen-share parts: (a) the **camera bubble sits bottom-right** — so bottom-left is
> the safe default and bottom-right will cover his face; (b) the background is often a **white
> page** — text-on-footage with no backing panel vanishes. Every card template carries its own
> dark card for this reason; if you build a new text overlay, give it a backing card or scrim so
> it survives a white background. Always eyeball a real frame at the actual insertion time.

Print the plan, then proceed (same render-first contract as video-rough-cut — revisions are cheap):

```
0:33.3  lower-third  "Dan Vega · Spring Developer Advocate"  bottom-left  6.0s
        (name at orig 40.2s → out 34.9s via trim map, − 1.8s reveal offset)
```

## Step 2 — Render each graphic

One-time setup per machine: `cd <skill>/scripts && PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install`
(uses the system Chrome via `channel: "chrome"` — no browser download).

```bash
node <skill>/scripts/render.mjs \
  --template <skill>/assets/templates/lower-third.html \
  --params '{"name":"Dan Vega","role":"Spring Developer Advocate"}' \
  --duration 6 --fps 30 \
  --out /tmp/video-motion-graphics/$NAME/g1 \
  --mov /tmp/video-motion-graphics/$NAME/overlays/lower-third.mov
```

Match `--fps` to the source video's frame rate (`ffprobe … r_frame_rate`), and match resolution
with `--scale`: templates lay out at 1920×1080, so pass `--scale <videoWidth/1920>` (`--scale 2`
for 4K) — same layout, sharper raster.

## Step 2.5 — Zooms (pure ffmpeg, no template)

Zooms transform the **base video** and must happen *before* the overlay pass (cards must not
zoom). Split the timeline into contiguous segments — the segments must tile the full duration,
no gaps — apply a zoom (or nothing) per segment, concat. Both recipes are resolution-agnostic
and keep the zoom center x-centered with the upward bias `(ih-oh)*0.3` for natural headroom.

**Hard punch** (constant 110% for the whole segment):

```
[b]trim=start=A:end=B,setpts=PTS-STARTPTS,scale=iw*1.10:ih*1.10,crop=iw/1.10:ih/1.10:(iw-ow)/2:(ih-oh)*0.3[v1];
```

**Slow push** (100→106% over the segment, D seconds at FPS):

```
[c]trim=start=B:end=C,setpts=PTS-STARTPTS,zoompan=z='min(1+0.06*on/(D*FPS),1.06)':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)*0.3':d=1:s=${W}x${H}:fps=${FPS}[v2];
```

`${W}x${H}` is the video's **native** size from ffprobe — zoompan's `s` defaults to 1280×720 and
will silently downscale if omitted (see pitfalls). Concat the segments (`[v0][v1][v2]concat=n=3`)
into `[base]`, then run the Step 3 overlay chain on `[base]` — one filter graph, one encode.
Audio needs no work: zooms don't change the timeline, so `-map 0:a -c:a copy` still holds.

**Code zoom-to-region** (screen-share) — the punch-in rule says never *blindly* zoom screen-share,
but a *targeted* zoom into the exact code being discussed is one of the best moves for code (makes
small text readable on mobile). It's the same segment/concat mechanism, but the crop is aimed at a
rectangle center `(CX,CY)` given as **fractions of the frame**, not center-with-headroom. Get the
region by extracting the frame (`ffmpeg -ss <t> -frames:v 1`) and reading the box off it — the same
fractional coords the `spotlight` template uses, so a zoom and a spotlight can share one measurement.

```
# hard zoom to region: zoom Z centered on (CX,CY), clamped so the crop stays on-frame
[seg]trim=start=A:end=B,setpts=PTS-STARTPTS,scale=iw*Z:ih*Z,crop=${W}:${H}:'min(max(CX*iw-${W}/2,0),iw-${W})':'min(max(CY*ih-${H}/2,0),ih-${H})',setsar=1[vN];
# smooth push to region (1→Z over D seconds)
[seg]trim=start=A:end=B,setpts=PTS-STARTPTS,zoompan=z='min(1+(Z-1)*on/(D*${FPS}),Z)':x='min(max(CX*iw-(iw/zoom)/2,0),iw-iw/zoom)':y='min(max(CY*ih-(ih/zoom)/2,0),ih-ih/zoom)':d=1:s=${W}x${H}:fps=${FPS},setsar=1[vN];
```

Z≈1/regionWidthFraction gets the region to roughly fill the width (e.g. a box ~45% wide → Z≈2.2).
`setsar=1` on every segment keeps concat happy. **For readability, often a `spotlight` overlay
(dim + highlight, no zoom) beats a zoom** — it keeps the surrounding code visible and never
softens the pixels. Reach for the zoom only when the code is genuinely too small to read.

**Speed-ramp** (screen-share) — timelapse a long typing/boilerplate/scrolling stretch instead of
cutting it. This is the one move that **changes the timeline**, so it reflows every later
timestamp:

```
[seg]trim=start=A:end=B,setpts=(PTS-STARTPTS)/S[vN];   # video S× faster
[aseg]atrim=start=A:end=B,asetpts=PTS-STARTPTS,atempo=S[aN];   # audio must match (atempo≤2, chain for more)
```

⚠️ A ramp over `[A,B]` at speed `S` removes `(B−A)(1−1/S)` seconds from the output. **Do the ramp
FIRST, then compute every overlay/zoom time in the post-ramp clock** (extend `to_out` with the
ramp shift), or only ramp a tail stretch with nothing sync'd after it. Ramping mid-plan without
reflowing is the fast way to desync everything downstream. Audio is NOT `copy` here — it's ramped
and concatenated alongside the video, then mapped as `[aout]`.

## Step 3 — Composite in one pass

One ffmpeg run overlays every graphic at its timestamp; `setpts` delays each PNG sequence to its
start time, `eof_action=pass` lets the video continue after the overlay ends:

```bash
ffmpeg -y -hwaccel videotoolbox -i video.mp4 \
  -framerate 30 -i g1/f_%04d.png -framerate 30 -i g2/f_%04d.png \
  -filter_complex "\
[1:v]setpts=PTS-STARTPTS+2.0/TB[g1];\
[2:v]setpts=PTS-STARTPTS+107.0/TB[g2];\
[0:v][g1]overlay=eof_action=pass[v1];\
[v1][g2]overlay=eof_action=pass[outv]" \
  -map "[outv]" -map 0:a -c:v libx264 -preset fast -crf 19 -pix_fmt yuv420p -c:a copy out.mp4
```

## Step 4 — Verify, then deliver

- Extract a frame from the composite at the mid-hold of EACH graphic and look at it: text
  correct, nothing important occluded, brand colors intact.
- **For any graphic synced to audio, verify the sync — not just occlusion.** Extract a frame at
  the *reveal* moment (render_start + REVEAL_OFFSET) and confirm the key text is fully on screen
  exactly when it's spoken. Off by a beat = re-derive render_start from the word-level timestamp,
  don't eyeball it.
- Deliver into the **directory the skill was launched from** (the cwd) — NOT `/tmp`, which is
  ephemeral and hidden in Finder. Save to `<cwd>/video-motion-graphics/<name>/<name>_gfx.mp4`, `open` it.
  (`/tmp/video-motion-graphics/<name>/` stays the scratch/working dir; the final artifacts get copied out.)
- Keep `overlays/*.mov` next to it — pre-timed ProRes 4444 with alpha, drag-into-Premiere ready —
  and mention them in the report.
- Report: plan as executed, per-graphic timestamps, where the overlays live.

## Authoring new templates

- 1920×1080, transparent background, one self-contained HTML file.
- Implement `window.setParams(obj)` and `window.seek(t, total)`. **All animation must be computed
  from `t` inside `seek`** — CSS animations/transitions are nondeterministic under frame capture.
- Reuse the brand tokens: card `rgba(13,17,10,0.88)`, border `rgba(255,255,255,0.10)`, radius
  14px, accent `#8ce99a`, prompt `#69db7c`, text `#f4f7f2`, dim `rgba(255,255,255,0.38)`,
  traffic lights `#ff5f57 #febc2e #28c840`, mono "SF Mono"/Menlo, sans -apple-system/Inter.
- Easing: `easeOutCubic` for entrances, `easeInCubic` for exits, steps for typing.

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
- (2026-07-23) A multi-part recording (video-rough-cut of `_01..\_05` parts concatenated) has per-part
  trim maps: `t_out = to_out_part(t) + sum(prior parts' rough durations)`. Build the combined map
  before placing anything; the seams themselves are the natural chapter boundaries for
  transitions/section-titles.

## What this skill does NOT do

- **Passive** screencasts with nothing to call out — if there's no error, no key line, no chapter
  structure, a screen recording doesn't need graphics. But structured *coding walkthroughs* (like
  the 02 videos) ARE in scope: chapters, endpoint callouts, and code spotlights/zooms on the beats
  that matter. (Superseded the earlier "talking-head only" note once code moves were built.)
- Cutting or pacing (video-rough-cut), captions, music, thumbnails (video-packaging).
- Full-screen b-roll or animated code walkthroughs — possible future sibling skill.
