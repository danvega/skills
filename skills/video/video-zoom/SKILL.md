---
name: video-zoom
description: >-
  Add zooms to talking-head footage after the rough cut: punch-ins at jump cuts so a cut reads
  as a camera change, and slow pushes on key lines, all centered on Dan's face so the frame never
  zooms into empty space. Renders them into the preview and writes them into the Premiere XML as
  editable Scale and Position keyframes. Use when Dan asks for zooms, punch-ins, pushes, "make
  the talking head more dynamic", or when the video-edit orchestrator reaches the zoom stage.
  Needs an approved rough cut (video-rough-cut). Not for zooms into screen recordings yet, and
  not for graphics (video-motion-graphics).
---

# Zooms

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

Numbers live in `style/style.json` under `zoom`: punch scale (1.10), push scale (1.06), push
length (2 to 8 s), at least 6 s between zoom changes, at most 6 changes a minute, max 1.25.

## 1. Options

```bash
$V zooms --work WORK
```

Read `WORK/cues/zoom-options.md`:

- **Punch-ins** are proposed at every jump cut (a cut inside one clip that skips more than
  0.3 s), alternating in and out, spaced by the rule above. A new clip starts at normal framing.
  They are kept unless you drop them.
- **Push lines** are every sentence 2 to 8 s long that sits inside one kept range. Choose the few
  that carry the point: the hook, a key claim, a punchline, the question at the end. Two or three
  in a short video is plenty. A push cannot go on a range that is already punched in.

## 2. Decide

Write `WORK/cues/zoom-decisions.json`:

```json
{"pushes": ["s1", "s6"], "drop": ["z3"]}
```

Drop a punch-in when the cut is not visible (Dan barely moved) or when two zoom changes would
land too close together for the content.

## 3. Build

```bash
$V zooms --work WORK --build
```

Checks the budget, finds Dan's face in each zoomed range (Apple Vision, cached), and writes
`WORK/cues/zoom.json`. Every zoom scales around the face, so the face stays where it is on
screen and the frame never shows an edge.

Then `$V preview --work WORK` renders the zooms into the preview (and runs the usual checks),
and `$V export --work WORK --name NAME` writes them into the Premiere XML. In Premiere they are
plain Scale and Position values or keyframes in Effect Controls, so Dan can change or delete any.

## 4. Check

Make a contact sheet just before and after each zoom change and compare face size against the
source frame at the same moment. Zoom levels should be within a few percent of the plan and the
face should not move more than about 1% of the frame.

## Gotchas

- (2026-10-07) Premiere reads Basic Motion keyframe times as SOURCE frames (counted from the
  media start), not frames within the clip. vedit writes them that way.
- (2026-10-07) Comparing preview face size against the first frame is noisy (head pose changes).
  Compare against the source frame at the same moment instead.
- (2026-10-07) Wispr Flow puts an invisible window over the middle of Premiere's timeline. When
  driving Premiere, select clips with the playhead (Down arrow, then D) instead of clicking them.
