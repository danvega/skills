---
name: video-sfx
description: >-
  Add sound effects to an edit, timed to the motion graphics: a pop when an icon or link card
  lands, a whoosh as the list panel slides in, a tick as each list item appears. Uses Dan's
  approved sound kit from Epidemic Sound, mixes it into the preview, and puts it on its own
  stereo track pair in the Premiere XML. Use when Dan asks for sound effects, SFX, pops,
  whooshes, or "make the graphics sound good", when choosing or changing the sound kit, or when
  the video-edit orchestrator reaches the sound stage. Run after video-motion-graphics. Not for
  background music (video-music).
---

# Sound effects

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

## The kit

`style/sound/kit.json` lists the approved sounds by role (pop, whoosh, tick) with their Epidemic
Sound id, title, and the peak level each plays at (pop −16, whoosh −18, tick −20 dBFS, well under
Dan's voice). The WAV files sit next to it and are not committed. If one is missing, download it
again by id with the Epidemic Sound MCP (`DownloadSoundEffect`, WAV) and save it under the kit's
file name.

Which graphic gets which sound, and the limits (0.3 s between sounds, 14 a minute), are in
`style/style.json` under `sfx`.

## Run

```bash
$V sfx --work WORK
$V preview --work WORK
$V export --work WORK --name NAME
```

`sfx` reads the built graphics plan, places a sound on each event, drops any that crowd the
limits, writes `WORK/cues/sfx.json`, and copies the kit into `WORK/sfx/` at its set levels.
The preview mixes them under the dialogue without lowering it. The XML puts them on a stereo
track pair under the dialogue, one clip per sound, named for the graphic it belongs to.

Rerun `sfx` whenever the graphics change: the sounds follow the graphics.

## Changing a sound

When Dan wants a different sound for a role:

1. Search with the Epidemic Sound MCP (`SearchSoundEffects`, keep UI sounds under about 1 s).
   Use `SearchSimilarToSoundEffect` with the current id to stay close to what he liked.
2. Let him hear candidates in context: swap one into the kit, run `sfx` and `preview`, and point
   him to the moment.
3. When he approves, download the WAV, update the entry in `kit.json` (id, title, file), and
   adjust `peak_db` if he says it is too loud or too quiet.

## Check

Mix the plan over silence to confirm each sound starts at its planned time, and check the
loudest sound effect peak stays at least 12 dB under the dialogue peaks.

## Gotchas

- (2026-10-07) Kit WAVs from Epidemic are 96 kHz. They are resampled to 48 kHz when copied into
  the project, so Premiere and the preview match the dialogue.
- (2026-10-07) Very short sounds read as −70 LUFS (too short to measure). Levels use peak dBFS.
