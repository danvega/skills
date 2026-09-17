---
name: video-motion-graphics
description: >-
  Add branded overlays and targeted camera moves to recorded YouTube footage, including
  talking-head and coding walkthroughs. Use for lower thirds, chapter titles, callouts,
  spotlights, or zooms. Preview short sequences before a full composite. Use video-visual-story
  for B-roll and full-screen explainers, and video-code-animation for animated code changes.
---

# Motion Graphics

Help viewers follow what Dan is saying and showing. Add a graphic where it clarifies the footage;
ordinary screencasts do not need decoration. Both talking-head and structured code demos are in
scope. Preserve Dan's bottom-corner card preference and leave chapter stingers to his final edit.

## Inputs and shared timing

Resolve the video, project folder, and any explicit requests. Prefer the rough-cut project's
`00_Project/edit/edit.json` and `transcript.output.json`. Read the mapped transcript directly:
its times are already on the delivered rough-cut clock. Do not map them a second time.

For source-clock anchors, use `video-rough-cut/scripts/pipeline.py map` with the exact clip ID.
Missing maps do not establish matching clocks. For an older cut without a manifest, recover a
verified map from its edit evidence or transcribe that cut directly. Only snap a boundary anchor
within 0.3 seconds after listening and confirming that the word survived; never snap deleted takes.

Sample frames across the WHOLE recording and inspect each planned insertion interval. Modes,
camera bubbles, autocomplete panels, and terminal windows change within clips. If a graphics
plan came from `video-visual-story`, use it instead of inventing a second competing plan.

## Choose the graphic by its job

| Treatment | Use and defaults |
|---|---|
| `lower-third.html` | Name/role introduction; about 6 s. Once per series, at the spoken self-intro. Skip continuation videos. Standalone videos without an intro can use an early clean scene. |
| `section-title.html` | A real chapter change; about 4 s. Bottom-left, or right if clear. Not every subtopic. |
| `callout.html` | A useful repo, URL, or version; about 5 s. Shorten the visible label if needed for readability. |
| `subscribe-nudge.html` | Once at a natural beat around 60 to 75% through, provided it does not cover the explanation. About 6 s. |
| `spotlight.html` | Dim around a measured code/result rectangle; about 4 to 5 s. Keeps context visible. |
| Talking-head punch/push | 110% punch at a cut, or 100 to 106% push over an emphasis line. Return to normal between moves; at most every second or third cut. |
| Targeted code zoom | Only when the relevant text needs magnification. Measure the real region; never blindly center-zoom code. |

Templates are in `assets/templates/`. Read [rendering.md](references/rendering.md) for parameters,
render commands, preview compositing, alpha handling, and caching. Read
[camera-moves.md](references/camera-moves.md) only if camera moves are planned.

A speed change belongs in rough-cut decisions BEFORE graphics placement. Rebuild the manifest
and mapped transcript, then re-anchor the graphics. Never add an untracked speed change here.

## Plan, preview, finish

1. Save a `graphics.json` plan next to the project graphics, using the schema in rendering.md.
   Record the base video's identity and the edit manifest ID, plus the narration anchor and
   intended purpose of each graphic. Explicit requests override automatic placement.
2. Extract real frames at candidate times and render single-frame posters first. Inspect backing
   contrast, text length, safe areas, and the actual code/output underneath. On IntelliJ the full
   bottom panel can be occupied: shifting the moment is often better than swapping corners.
3. Render each needed graphic and make a short composite preview including surrounding narration.
   Watch entry, reveal, hold, exit, and sync. A still frame cannot verify spoken synchronization.
   Fix only the affected asset or placement and repeat its short preview.
4. Once those checks pass, make one full composite if that is the requested deliverable. For an
   asset-only request, deliver the assets and placement plan without encoding the entire video.
   Save `<project>/01_Footage/<name>_gfx.mp4`; overlay masters and their plan go into
   `<project>/03_Graphics/overlays/`. With no project, use `<source_dir>/video-motion-graphics/<name>/`.
5. Verify the final output's duration, native resolution, and a few actual graphic moments.
   Report placements, file paths, preview checks, and unresolved editorial issues. Do not call
   untimed overlay files “pre-timed”; their positions live in the plan.

Proceed through reversible previews and rendering without extra confirmation. For a genuinely new
visual direction, show a representative preview for feedback; avoid requiring a new style decision
on every routine lower third. Keep accepted templates reusable.

## Straight after a rough cut

`video-rough-cut` hands off to this skill in the same run, without Dan asking. In that case the
full composite `<name>_gfx.mp4` is the deliverable, next to the untouched `<name>_rough.mp4`.
Still run the poster and short preview checks, but do not pause for feedback. Use accepted
templates only. If a moment calls for a new visual direction, skip it and describe the idea in
the report. Finish with one message that covers both files.

## Reveal timing and placement

Sync the important REVEAL to the spoken phrase, not the first frame of the animation.
`render_start = output_clock_anchor - reveal_offset`. If that is negative, shorten the entrance
or move the graphic to a later meaningful beat; do not silently truncate a meaningful reveal.

| Template | Approximate reveal offset |
|---|---|
| Lower third | 1.8 s for name; 2.15 s for role |
| Callout | 0.42 s + min(1.1 s, value length × 0.045 s) |
| Section title | 0.78 s |
| Subscribe nudge | 1.9 s |
| Spotlight | 0.4 s for box; 0.5 s for label |

Recheck these against `seek()` when a template changes. Require a dark backing panel/scrim for
text on light screen shares. Camera bubbles are often bottom-right; do not assume they are always
present. Chapter cards can move a few seconds to avoid a terminal payoff. Precisely synchronized
explanations should instead change layout or use a dedicated insert.

## Authoring

Use self-contained 1920×1080 HTML with `window.setParams(obj)` and `window.seek(t,total)`.
All animation is a deterministic function of `t`; no CSS transitions or real-time timers.
Render at `--scale 2` for 4K overlays. Transparent masters use ProRes 4444; full-frame inserts
usually need only MP4. Reuse colors, type, and easing, while choosing composition for the content.
The established cards use background `rgba(13,17,10,0.88)`, accent `#8ce99a`, text `#f4f7f2`,
SF Mono/Menlo plus system sans, ease-out entrances, and ease-in exits.

Historical failures are retained in [history.md](references/history.md). Update the applicable
current rule after learning from a run; do not append competing operational instructions here.
