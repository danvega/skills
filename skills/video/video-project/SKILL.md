---
name: video-project
description: >-
  Create a new YouTube video project folder in ~/youtube from Dan's 2026Template: the numbered
  folders (00_Project to 07_raw), the template Premiere project renamed to the video's name, and
  an edit/ work folder set to the right channel brand. Use when Dan says "new video", "set up a
  project for X", "create the folder for my next video", or when the video-edit orchestrator
  starts a video that has no folder yet. Never renames, moves, or overwrites an existing project.
---

# New video project

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

## Ask

1. **Name.** Derive the folder from the video's name: PascalCase, strip spaces and
   punctuation, keep digits and capitalized acronyms
   ("Spring AI 2.0 Crash Course" → `SpringAI20CrashCourse`, "Claude Code: Plan Mode" →
   `ClaudeCodePlanMode`). State the name you picked. Don't ask about it.
2. **Channel.** Which brand (`ls style/brands/`): `dan-vega` for his own channel, `broadcom` for
   Broadcom. Do not guess this. It decides the graphics look.

## Create

```bash
$V new NAME --brand BRAND
```

It copies `~/youtube/2026Template` to `~/youtube/NAME`, renames
`00_Project/NewProjectTemplate.prproj` to `NAME.prproj`, and creates `edit/project.json` with the
brand. It refuses a name that already exists. If Dan wants to reuse a name, he renames the old
folder first (for example to `NAMEDRAFT`), and only when he asks.

## The layout

| Folder | Holds |
|---|---|
| `00_Project` | the Premiere project |
| `01_Footage` | footage used in the edit (the template's `endcard.mp4` is already here) |
| `02_Audio`, `03_Graphics` | audio and graphics Dan adds by hand |
| `04_Exports` | finished videos, shorts, teasers |
| `05_Transcripts` | transcripts to share or publish (srt, vtt, txt, json, clean.md). Every transcript of a finished or exported video goes here |
| `06_Thumbnails` | thumbnail work |
| `07_raw` | raw recordings. Dan drops Ecamm recordings here, and `vedit raw` renames them to `<Name>_01.mp4`, `_02`, ... |
| `edit` | the vedit work folder: transcripts, cut list, cues, renders, preview, XML |

## Report

The project path, the Premiere project path, and where to put recordings (`07_raw`). Then the
next step: record, drop the files in `07_raw`, and run the `video-edit` skill.
