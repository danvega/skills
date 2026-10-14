---
name: video-rough-cut
description: >-
  Rough-cut raw YouTube recordings: remove dead air, fillers, stutters, retakes, false starts,
  spoken slates ("cut that"), and wordless code entry, while protecting speech and demo results.
  Scripts find candidates and build the cut; Claude decides the judgment calls; Dan approves the
  plan on a review page before anything renders, then gets a verified 720p preview. Use when Dan
  says "rough cut this", "cut the dead air", "clean up these takes", "first pass", or when the
  video-edit orchestrator reaches the rough-cut stage. Do not use for graphics, zooms, B-roll,
  captions, or the final Premiere export (later video-* stages).
---

# Rough cut

The cut list (`edl.json`) is the only source of truth. You never type a timestamp: you pick
words and pauses, and `vedit` turns them into frame-aligned cuts that cannot land inside a word.

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

## 1. Transcribe

Run the `video-transcribe` skill on every source, in the order they play. Its work folder is
this stage's `--work` folder too.

## 2. Find candidates

```bash
$V candidates --work WORK --order SRC1 SRC2 ... [--mode screen-share] [--mode-for SRC=screen-share]
```

Source ids are in `WORK/sources.json`. Pick the mode per source: `talking-head` for camera
footage, `screen-share` for screen recordings. Pause rules differ by mode (see `style/style.json`).

Read `WORK/proposals/candidates.md`. Items marked `cut` are mechanical (fillers, stutters,
ordinary pauses). Items marked `review` need your judgment.

## 3. Decide

Read [judgment.md](references/judgment.md), then decide every `review` item using the sentence
context in candidates.md and `WORK/transcript/<src>.phrases.md`. For a long silent stretch in a
screen recording, look before deciding:

```bash
$V sheet SOURCE_FILE --at START MIDDLE END --out WORK/review/c12.png
```

Write `WORK/proposals/decisions.json`:

```json
{"decide": {"c3": "cut", "c7": "keep", "c9": {"action": "cut", "leave": 0.7}},
 "cuts": [{"src": "hello", "w0": 40, "w1": 52, "reason": "tangent Dan asked to drop"}]}
```

`cuts` are extra word ranges the script did not find. Use them sparingly, with a reason.

## 4. Gate 1: Dan approves the plan

```bash
$V plan --work WORK
```

It refuses to run while any `review` item is undecided, and refuses a cut list that fails
validation. Open `WORK/review/cut-plan.html` for Dan. It shows every word, with cut text struck
through and a cut id on each. Report the before and after length and anything you were unsure
about. When Dan says "keep c12" or "also cut X", edit decisions.json and run `plan` again.
Never render before Dan approves.

## 5. Preview and verify

```bash
$V preview --work WORK
```

This renders `WORK/preview/rough.mp4` (720p) and verifies it: audio and video in sync, a
re-transcription of the preview matching the planned words, and no clicks at joins. A
non-zero exit means a check failed. Read `WORK/qa/preview.json`, fix the cause, and run it
again. Do not hand Dan a preview that failed.

## 6. Export for Premiere

```bash
$V export --work WORK [--name PROJECT_NAME]
```

Writes `WORK/export/<name>.xml` (FCP7 XML; in Premiere: File > Import). Each cut is its own
clip pointing at the original footage with source in and out points, so Dan can extend any trim.
No cut markers by default (Dan does not need them). `--markers` adds one at each join
where words were removed, naming them. Media arrive as
master clips in bins at the top of the project, matching Dan's project template (`01_Footage`,
`02_Audio` with `Music` and `Sound FX`, `03_Graphics`, `Sequences`). Each file appears once. For a
test import, add `--bin NAME` to wrap everything in one bin, so an old version is one bin to delete. The command reads the XML
back and compares it with the cut list. A non-zero exit means they differ: do not hand it over.

Report: original and new length, cuts by kind, the review items you decided and how, and the
preview and XML paths.

## Gotchas

- (2026-10-07) Camera files report an average frame rate like 12490/417 that differs slightly
  from the real 30 fps. vedit checks actual frame timing before calling a file VFR, and uses
  the real rate for the sequence.
- (2026-10-07) Never join AAC audio by stream copy. It clicks about 100 ms after each join and
  drifts. The preview keeps audio as PCM per piece with 20 ms fades and encodes AAC once.
- (2026-10-07) Premiere Pro 2026 silently drops stereo audio written as one clip on one track,
  and OpenTimelineIO's FCP7 writer does the same. vedit writes stereo "exploded" (two linked
  tracks, as Premiere does). Tested by importing into Premiere: V1 and stereo A1 both arrive.
- (2026-10-07) The preview check ignores one-word transcription noise ("4" vs "for") but
  reports two or more words dropped or doubled. Treat any reported issue as a real cut problem.
- (2026-10-07) Importing a second XML into the same project: Premiere reuses the sound effect,
  music, and graphics clips it already has, so the new import shows only `01_Footage` and
  `Sequences`. The timeline still links every clip. Fresh master clip ids did not change this.
  A first import into a project shows all bins.
- (2026-10-07) V2 stays empty for Dan's color adjustment layer. Premiere keeps the empty track.
