---
name: video-edit
description: >-
  Edit a talking-head YouTube video from raw recordings to an almost finished Premiere timeline,
  by running the video-* skills in order: transcribe, rough cut (Dan approves the plan), then
  zooms, motion graphics, and sound effects, with background music in parallel, then one checked
  preview and the Premiere XML. Asks its questions once at the start. Use when Dan says "edit
  this video", "edit my recording", "run the full edit", "take this to Premiere", or drops new
  recordings and wants the whole pipeline. For one stage only, use that stage's skill.
---

# Edit a video

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

You run the stages. Each stage's skill holds its rules. Read a stage's SKILL.md when you reach
it and follow it, with the changes below. Dan wants the video as close to done as possible
before he opens Premiere, and every piece still editable there.

## 0. Set up (ask everything once)

**Project.** Videos live in `~/youtube/<Name>/` (layout in `video-project`). If there is no
folder yet, run `video-project` first. Sources are the recordings in `07_raw`. Work folder:
`<project>/edit`.

**Rename recordings first.** Ecamm names files by date. Before anything reads them:

```bash
$V raw ~/youtube/<Name>
```

It renames them to `<Name>_01.mp4`, `_02`, ... in recording order (new ones continue the
numbering) and logs the Ecamm names in `07_raw/renames.json`. Never rename a source after it is
transcribed: the work folder records sources by path.

**Ask in one message** (skip what is already known):

1. **Channel**, if `edit/project.json` has no brand: `dan-vega` or `broadcom` (`$V brand`).
2. **Recordings and order**, if `07_raw` has more than one: confirm which ones and in what order.
3. **Music:** yes or no for this video. Dan does not always want it.
4. **Link** for the GitHub popup, if he will point to the description. Never invent a URL.
   Also any links to articles or tweets he cites, if he has them (saves a search).
5. **Anything he already knows** should be cut or kept.

Then work without stopping until Gate 1.

## 1. Transcribe

Run `video-transcribe` on the sources.

## 2. Rough cut (Gate 1)

Run `video-rough-cut` through step 5: candidates, your decisions, the plan page, and Dan's
approval. **Gate 1 is the only stop in the middle.** Nothing after it is worth building on a
cut Dan has not approved. Run its preview to catch cut problems early (sync, words, clicks),
but do not ask Dan to watch it. Skip its export step: the export comes at the end.

## 3. Build (after Gate 1)

Two branches at once:

- **Main thread, in order** (each needs the one before it):
  1. `video-zoom`: options, your decisions, build. Graphics are placed beside Dan's face after
     the zoom, so zooms come first.
  2. `video-motion-graphics`: options, your decisions (with the link from setup), build. The
     brand comes from `project.json`.
  3. `video-broll-research`, when Dan cites an article, post, docs, or a tweet: find each real
     source and capture it, then **stop for Dan to approve the sources** on
     `review/research.html` before building. Skip it when nothing is cited.
  4. `video-sfx`: follows the built graphics and source cards.
- **Subagent, only if Dan wants music:** start it right after Gate 1 with the Agent tool. Tell
  it the work folder and to follow `.claude/skills/video-music/SKILL.md` steps 1 to 4, but to
  stop before `preview`, and to report the track, the runners-up, and `bed_lufs`. It writes
  only `edit/music/` and `edit/cues/music.json`, so it cannot collide with the main thread.

Make each stage's decisions yourself, using its skill's rules. Dan reviews the result, not
each step. Skip each stage's own `preview`. One preview at the end covers all of them.

## 4. Preview and check

Wait for the music subagent, then:

```bash
$V preview --work WORK
```

It must pass (sync, words, clicks). Then do each stage's visual check from its skill: contact
sheets around zoom changes, graphics, and list slides. Fix what fails before Dan sees anything.

## 5. Export

```bash
$V export --work WORK --name NAME
```

`NAME` is the project name. It must exit 0. The XML puts bins at the top of the project
(`01_Footage`, `02_Audio`, `03_Graphics`, `Sequences`), V1 footage with zoom keyframes, V2 empty
for Dan's color adjustment layer, V3 and V4 graphics, A1 dialogue, A2 sound effects, A3 music.

## 6. Hand off (Gate 2)

Report in short lines:

- original and final length, and cuts by kind
- zooms, graphics, and sounds added, and anything dropped and why
- the music track, if any
- anything you were unsure about, with timestamps
- the preview (`edit/preview/rough.mp4`) and XML (`edit/export/NAME.xml`) paths

Dan imports the XML himself (File > Import in his project). Only drive Premiere if he asks, and
never in a real project without his go-ahead for that project.

## Feedback

Change the stage that owns the problem, then rebuild that stage and everything after it:

| Dan says | Change | Then rerun |
|---|---|---|
| a cut is wrong, keep or cut words | `proposals/decisions.json` (video-rough-cut) | plan, Gate 1, then everything after |
| a zoom is wrong | `cues/zoom-decisions.json` | zooms, graphics, sfx, preview, export |
| a graphic is wrong or misplaced | `cues/graphics-decisions.json` | graphics, sfx, preview, export |
| a sound is wrong | `style/sound/kit.json` (video-sfx) | sfx, preview, export |
| the music is wrong | a new track (video-music) | music, preview, export |

A changed cut makes zoom, graphics, sound, and music stale. `preview` and `export` refuse to run
on stale cues, so rebuild them. Approved choices that should hold for every video (a level, a
placement) go into `style/style.json` or the brand file, not into one project.
