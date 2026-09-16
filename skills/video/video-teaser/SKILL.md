---
name: video-teaser
description: >-
  Create a cinematic pre-release teaser from an in-progress developer video: a short montage
  with selected dialogue, demo glimpses, purposeful title cards, and sound design. Use for a
  teaser, movie-trailer-style preview, sneak peek, or coming-soon promotion. Uses available
  footage without waiting for the final export. Delivers video files and optional post copy;
  does not upload or schedule. Published-video clips and vertical shorts are separate workflows.
---

# Video Teaser

Make a miniature trailer for the video's central promise. Dan's direction: the earlier teaser
was just him talking with words over it. The default now is an EDITED SEQUENCE with a dramatic
shape, visual evidence, and intentional sound. A continuous excerpt with automatic word-pop
captions is only appropriate when Dan specifically asks for that simpler format.

“Cinematic” means well-chosen images, rhythm, contrast, and sound that support the actual topic.
Keep Dan's natural voice. Technical stakes can be compelling without a fake disaster, invented
results, generic hacker stock footage, or an exaggerated trailer-announcer performance.

## Resolve the project and material

Find the intended project under `/Users/vega/youtube/`. If “this video” is ambiguous, ask for its
title or project folder while preparing reusable treatments. Do not choose an unrelated project.

Use whichever useful material already exists, stating the source:

1. A preview, rough, or WIP export in `04_Exports/`, or the working cut in `01_Footage/`.
2. Raw recordings in `07_raw/` or `01_Footage/`, resolving the last complete genuine take.
3. Existing demo captures, code animations, explainer inserts, screenshots, and title assets.

Read `script.md`, `shot-list.md`, the brief/demo plan, and visual-story plan when available.
Identify the question, stakes, proof, and full video's payoff. Show enough of the result to make
the promise credible; withhold the full method or resolution. Do not hide every useful glimpse
just because the old skill said to avoid anything implying the answer.

Use an exact-source cached transcript. `video-rough-cut/scripts/pipeline.py transcribe` extracts
only audio and reuses matching ASR results. A rough cut's mapped transcript is valid only for
that exact cut. Sources can have different clocks: every selected line needs its own source path
and source in/out points. Trailer output timing is a new clock.

Work in `<project>/03_Graphics/teaser/`. Deliver to `<project>/04_Exports/teaser/`.
Keep the plan, dialogue selections, source provenance, and editable card/caption files there.

## 1. Design the trailer before rendering

Target roughly 25 to 45 seconds, always under 60 unless Dan requests another format. A strong
shorter cut is fine. Choose a structure fitting the material, for example:

| Part | Job | Possible picture/sound |
|---|---|---|
| Cold open | Create a question immediately | A real failure, surprising demo result, or Dan's sharpest line; a brief sound or silence |
| Stakes | Make the problem matter | Relevant screen evidence under a short dialogue excerpt |
| Escalation | Suggest what the video investigates/builds | A few distinct demo or explainer glimpses, cutting more tightly as the idea develops |
| Turn | Hint at the change or discovery | A revealing image, a short title, or a pause that changes the rhythm |
| Promise/title | Leave a clear reason to watch | The video's title or concise promise, “Coming soon,” and enough hold to read |

This is a useful shape, not five compulsory cards or fixed timestamps. Use a small number of
strong moments; let a key image or line breathe instead of speeding through everything.

Save `trailer-plan.json` and a readable shot table: output time, picture, dialogue, card text,
audio cue, source in/out, and purpose. Write the withheld resolution separately for the editor.
Choose dialogue from different moments when useful, but preserve what Dan actually meant.
Do not splice words into a sentence he did not say or manufacture a reaction to another event.

## 2. Build the picture and audio together

Use real B-roll as the visual backbone around selected on-camera lines. Dan can continue speaking
while the picture cuts to the thing he is discussing. Plan those audio/picture overlaps explicitly;
the visual cut need not occur at the same time as the dialogue cut.

- Show the actual demo, relevant code change, result, or a purpose-built explainer. Route missing
  explanatory visuals to `video-visual-story` and exact code changes to `video-code-animation`.
- Use a restrained small number of full-screen title cards to frame a question, turn, or title.
  Keep card copy short. Do not replace the entire narration with a series of animated words.
- Vary shot scale where it helps: face, readable detail, wider context. Preserve screen readability.
  Keep 16:9 by default, including a pure talking-head source. Reframing is a deliberate variant.
- Cut on a meaningful visual action, sentence beat, or musical event. Favor clean cuts; use a
  transition only when it communicates a shift. No automatic zoom/whoosh on every shot.
- Use local music with suitable permission if available: establish a pulse, build, then leave
  space for the final line/title. Duck it under dialogue. Silence can be a strong turning point.
- Add a few motivated effects (a real click, short impact, or transition cue) if they help. Keep
  speech intelligible and avoid piling effects on each edit. Preserve provenance for every track.
  If no suitable music is available, finish a deliberate dry edit and identify the missing asset;
  do not download an arbitrary copyrighted movie score or claim it is cleared.

Dan liked the CFML trailer's visual direction but found its stops and audio edits janky. Keep
musical continuity through short pauses, preserve natural breath/reverb tails, and use brief
edge fades on dialogue. Ease music ducking in and out; do not jump its level at each sentence.
A continuous sound bed and fewer purposeful picture changes can connect excerpts more naturally
than repeated face/code cutaways. Save a hard silence for a deliberate, earned story beat.

The bundled `scripts/montage.py` renders independent picture shots and placed dialogue/music/SFX
tracks, caches visual shots, ducks music during dialogue, and emits a teaser-clock transcript.
Read [trailer-edit.md](references/trailer-edit.md) for the plan schema and commands. It supports
clean cuts and audio overlaps, not a full Premiere replacement. Keep its limits explicit.

## 3. Preview a sequence, then finish the trailer

First render a representative roughly 8 to 12 second section including dialogue, a visual change,
and a title/turn if used. Show that concrete direction when the style is new. Continue source
selection and preparation while awaiting feedback; do not make a mandatory approval gate for
routine reversible edits. Then render the complete short trailer and watch it end to end.

For sound-off viewing, use readable phrase captions where dialogue carries essential information.
The bundled `assets/captions.html` accepts timed cues. Use the montage's output-clock transcript,
not source times. Captions should support the pictures and clear any existing labels or title
cards. They do not define the trailer's style. The teaser must still make sense when muted.

Check at normal playback speed:

- Does the first moment create interest without needing the tweet?
- Is there visual variety that actually develops the premise?
- Does every proof image support the claim being made?
- Are speech, music, and effects balanced on ordinary speakers?
- Do the cuts and title hold feel intentional? Is code readable at feed size?
- Does the ending promise something specific while preserving a reason to watch the full video?
- Are there clipped syllables, black flashes, repeated frames, or competing captions/cards?

Fix the affected shots, reuse their cached neighbors, and render again. Prefer one strong trailer
with a clear creative direction over several nearly identical talking-head excerpts.

## 4. Post copy and delivery

When teaser promotion is part of the request, write `teaser-post.md` with two or three distinct
ready-to-paste options. Keep each around 200 characters or less, in Dan's plain voice. Open the
same question as the trailer without explaining the full answer. No hashtags or invented links.
Use “Coming soon” or “Working on this one”; do not promise a date unless Dan supplied one.

Deliver `<name>_teaser.mp4`, the post copy when applicable, editable plan, and preview. Report the
source footage, duration, creative structure, proof shown, resolution withheld, and any missing
music/captures. Files only: do not upload, save social posts, or schedule anything. Dan posts
teasers by hand. A note to reply with the YouTube link after publication is fine; do not do it.

[Previous workflow](references/previous-workflow.md) is retained as history only. Its continuous
excerpt, mandatory word-pop captions, integer-FPS workaround, and automatic square crop have
been superseded by this trailer direction.
