---
name: video-project
description: >-
  Scaffold a YouTube project from Dan's local video template, creating a PascalCase folder
  and renaming the Premiere project file. Use when Dan asks for a new video project or
  wants the folders set up for a video. Do not use for choosing a topic (video-ideation),
  titles and thumbnail concepts (video-packaging), or editing footage (video-rough-cut).
---

# video-project

Scaffold a new video project folder from the standard template. Input: the video's
name in plain English (e.g. "Spring AI 2.0 Crash Course"). Output: a ready-to-edit
project directory under `/Users/vega/youtube/`.

## Paths

- **Template:** `/Users/vega/youtube/2026Template`
- **Projects root:** `/Users/vega/youtube/`

## Naming convention

Derive the folder name from the video name: PascalCase, strip spaces and all
punctuation (periods, hyphens, apostrophes, colons). Keep digits.

| Video name | Folder |
|---|---|
| Spring AI 2.0 Crash Course | `SpringAI20CrashCourse` |
| ChatClient vs ChatModel | `ChatClientVsChatModel` |
| Claude Code: Plan Mode | `ClaudeCodePlanMode` |

Acronyms already capitalized stay as-is (`AI`, `MCP`, `API`).

## Steps

1. Derive the folder name from the given video name (convention above). If the
   name is ambiguous, pick the obvious PascalCase form and state it — don't ask.
2. **Guard:** if `/Users/vega/youtube/<Folder>` already exists, stop and tell Dan.
   Never overwrite an existing project.
3. Copy the template:

   ```bash
   cp -R /Users/vega/youtube/2026Template /Users/vega/youtube/<Folder>
   find /Users/vega/youtube/<Folder> -name .DS_Store -delete
   ```

4. Rename the Premiere project file in `00_Project` to the folder name:

   ```bash
   mv /Users/vega/youtube/<Folder>/00_Project/NewProjectTemplate.prproj \
      /Users/vega/youtube/<Folder>/00_Project/<Folder>.prproj
   ```

   If `00_Project` holds a different single file than expected, rename whatever
   is there — the rule is "the one file in `00_Project` takes the project name",
   keeping its original extension.

5. Verify and report: list the new directory tree (folders `00_Project` through
   `07_raw`, `endcard.mp4` in `01_Footage`, the renamed `.prproj`) and give Dan
   the full path.

## Template layout (for reference)

```
00_Project/      NewProjectTemplate.prproj  → renamed to <Folder>.prproj
01_Footage/      endcard.mp4 ships with the template
02_Audio/
03_Graphics/
04_Exports/
05_Transcripts/
06_Thumbnails/
07_raw/
```

If the template itself changes (new folders, different project file), copy it
verbatim — this skill copies whatever the template contains and only ever renames
the file in `00_Project`.

## Editing handoff

When editing begins, `video-rough-cut` keeps its decisions, manifest, timing reports, and cache
in `00_Project/edit/`. Graphics and visual-story skills read that manifest and its mapped
transcript, and keep their editable assets/plans under `03_Graphics/`. The final Premiere
export still belongs in `04_Exports/`; shorts transcribe that exact export. Do not create empty
cache directories during scaffolding or modify the master template for these working files.
