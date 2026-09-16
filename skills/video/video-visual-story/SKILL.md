---
name: video-visual-story
description: >-
  Plan and produce B-roll and full-screen explainers for developer videos from the narration
  and real demo material. Use when Dan wants better visuals, a B-roll pass, diagrams showing
  how something works, or an illustrated explanation. Routes code changes to video-code-animation
  and overlays to video-motion-graphics. Does not cut speech or publish videos.
---

# Visual Story

Choose what a viewer needs to SEE to understand the point. Start with the explanation and its
payoff, then choose the visual form. Keep Dan's brand recognizable through color and typography;
composition can vary between evidence, diagrams, comparisons, and the recorded demonstration.

## Start from available material

Read the brief/demo plan and shot list if available. After recording, use the rough cut's
`00_Project/edit/edit.json` and `transcript.output.json`, plus frames from the footage.
For a final Premiere export, transcribe that exact export instead. Do not guess at clock mapping.
Before recording, anchor to narration phrases; assign exact times once the edit is stable.

Use `<project>/03_Graphics/visual-story/` for the plan, parameters, HTML, and previews. Deliver
full-frame inserts to `01_Footage/` and overlay masters to `03_Graphics/overlays/`. With no project,
use `<source_dir>/visual-story/<name>/`. Keep provenance and editable source alongside the assets.

## Build the visual plan

For important explanations, identify a visual only when it adds understanding or supplies proof.
No fixed insert quota or requirement to change the picture every few seconds. Keep the actual
screen recording when it already makes the point clearly.

For each useful insert, record:

- The exact narration phrase and its output-clock time, or an untimed phrase before filming.
- What the viewer should understand by the end.
- The visual action: what enters, moves, changes, and remains for reading.
- Source files, screenshot/recording path, or authoritative source URL and capture date.
- Intended duration, reading hold, and handles for the edit.
- Missing footage, layout constraints, and whether it is reusable.

Pick by purpose:

| Purpose | Treatment |
|---|---|
| Explain a request, lifecycle, or tool interaction | A small labeled flow with staged highlights and a moving request |
| Show a specific code change | Real source states through `video-code-animation` |
| Make a conceptual before/after contrast | A two-panel comparison revealing the outcome after the problem |
| Support a release/version claim | Real release notes or docs, focused on the relevant passage |
| Prove behavior | Capture the actual app action, request, error, test, or result |
| Direct attention in an already useful screen recording | `video-motion-graphics` spotlight or targeted zoom |

Use generated imagery only when an illustration genuinely helps; never fabricate product UI,
code, benchmark results, or documentary evidence. Keep externally sourced assets' origin and
usage permission with the plan. Do not add generic “person typing” footage just to fill silence.

## Produce with short feedback loops

1. Select the smallest useful set of treatments. Reuse accepted assets and structures first.
2. Build still frames with real content. For an existing treatment, proceed with the sensible
   default. For a new direction, show one representative sequence for feedback before producing
   a whole batch, while continuing independent preparation.
3. Render a short animation with the actual narration. Confirm the event is visible as it is
   described, text reads at phone size, and the result holds long enough to understand.
4. Fix the local sequence and preview again. Do not rerender the whole video for a small change.
5. Once local checks pass, add assets to the shared `graphics.json` placement plan and composite
   through `video-motion-graphics/scripts/composite.py`, or deliver inserts for Premiere if asked.
   Use one timing plan for overlays and inserts. Recheck anchors after an edit-manifest change.

The bundled `assets/templates/explainer.html` supports flow, comparison, and screenshot-evidence
modes using the existing graphics renderer. Read [treatments.md](references/treatments.md) when
using it. These are initial working treatments, not styles Dan has already approved. Code
animations continue using the existing token-aware blocks; do not rebuild that renderer here.

## Capture while the demo is ready

Add missing B-roll to the demo shot list before recording. For each capture: starting branch or
application state, action, visible payoff, framing, and recording filename. Capture clean before
and after states and a brief hold around the payoff while the demo is set up. Record without
unnecessary panels or cursor movement; make the relevant text readable at the intended framing.

Prefer reusing the demonstrated application and actual source files. If material is missing,
make the capture request concrete; do not silently substitute a fabricated screenshot.

## Finish and improve

Deliver the editable assets, short previews, and placement/provenance plan. Describe what each
visual explains, what was checked, and any missing captures. Keep two or three strong treatments
from a representative video as reusable examples after Dan's feedback. Track asset production
minutes, revision count, full-video encode count, and Dan's correction time. A technically valid
render alone does not establish that a visual is useful or matches his taste.
