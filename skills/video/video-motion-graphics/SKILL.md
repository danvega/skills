---
name: video-motion-graphics
description: >-
  Add Dan's motion graphics to a rough-cut talking-head video, driven by what he says: a lower
  third at his self-intro, a list reveal when he says "I'm going to cover three things" (his shot
  slides left, a branded panel slides in, items appear as he names them), a GitHub link popup when
  he points to the description, and icon pops when he names a tool. Renders 4K ProRes 4444
  overlays, composites them into the preview, and places them on V3 and V4 in the Premiere XML. V2 stays empty for Dan's color adjustment layer.
  Use when Dan asks for graphics, a lower third, a list, link or icon popups, or when the
  video-edit orchestrator reaches the graphics stage. Needs an approved rough cut. Run video-zoom
  first if zooms are wanted. Not for B-roll, diagrams, or code animations.
---

# Motion graphics

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

Templates live in `graphics/templates/` (1920x1080 HTML, `setParams` and `seek(t)`, all motion a
pure function of time). The renderer is `tools/render/render.mjs` (Playwright and system Chrome).
Numbers are in `style/style.json` under `graphics`. Spoken tool names map to icons in
`style/icons.json` (Simple Icons, CC0).

## 0. Brand

Each channel has a profile in `style/brands/` (name, role, theme, colors). `dan-vega` is the
terminal look for Dan's own channel and the default. `broadcom` is the light look matched to the
TrueSource animations: misty background, white cards, blue headings, and a navy-purple-red strip.
Ask Dan which channel the video is for, then set it once per project:

```bash
$V brand --work WORK broadcom
```

It is saved in `WORK/project.json`, and every later step uses it. Templates read the brand
through `graphics/templates/brand.js`. A new brand is a new JSON file, not a template change.

## 1. Options

```bash
$V graphics --work WORK
```

Read `WORK/cues/graphics-options.md`. The script finds:

| Graphic | Trigger | Track |
|---|---|---|
| lower-third | Dan says his name ("I'm Dan Vega") | V3 |
| list-reveal | "cover / talk about N things", then N spoken markers (one, two, three, finally) | V3, plus a slide on V1 |
| link-popup | a sentence with GitHub, repo, or link and "below" or "description" | V4 |
| icon-pop | the first mention of a tool in `style/icons.json`, at least 6 s apart, never during a list or link | V4 |

The lower third is shortened to leave before a list starts. A list ends at the next cut at the latest.

## 2. Decide

Write `WORK/cues/graphics-decisions.json`:

```json
{"link_url": "github.com/danvega/repo",
 "list_title": "Three things",
 "list_items": ["Docker Compose support", "A fast feedback loop in IntelliJ", "Claude writes my first tests"],
 "drop": ["g1"]}
```

- **link_url** must come from Dan or the project. Never guess one. Without it, drop the popup and
  say so.
- **list_items**: shorten each to what fits on one line, in Dan's words. Keep the count he said.
- **drop** anything that crowds the frame or repeats what is already on screen.

## 3. Build and check

```bash
$V graphics --work WORK --build
$V preview --work WORK
```

The build renders each graphic to `WORK/graphics/<id>-<kind>.mov` (4K ProRes 4444 with alpha)
and writes `WORK/cues/graphics.json`. The preview composites them over the zoomed cut.

Look before reporting. Make a contact sheet at each graphic's middle, at the start and end of every
list slide, and just after each graphic's scheduled end. Check: no black edge during a slide,
text readable at 720p, nothing over Dan's face, items appear as he says them.

Then `$V export --work WORK --name NAME`. In Premiere the overlays are ordinary clips on V3 and V4,
and the list slide is Position keyframes on Dan's clip.

## Gotchas

- (2026-10-07) An icon's time depends on the list window: shortening a list can free an earlier
  mention, so the icon moves. Read graphics.json for actual times before judging a frame.
- (2026-10-07) The installed ffmpeg has no drawtext or libass. All on-video text is rendered by
  the HTML templates.
