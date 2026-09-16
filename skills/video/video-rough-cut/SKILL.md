---
name: video-rough-cut
description: >-
  Produce a conservative rough cut from raw YouTube recordings: trim dead air and resolve
  retakes while protecting speech and screen activity. Use for a first pass, silence trimming,
  repeated takes, or recording cleanup. Saves a reusable edit manifest and transcript for
  graphics. Finishing, B-roll, captions, and publishing belong to other video skills.
---

# Rough Cut

Deliver a watchable first pass for Premiere, keeping natural pacing and the source resolution.
When uncertain about speech or a retake, keep it and flag it. Use the bundled pipeline for
mechanics; spend judgment on the edit rather than rebuilding shell scripts every run.

## Inputs and destinations

- Resolve the raw files and the project's folder. Ask for a file only if none is available.
- Classify footage as talking-head or screen-share. For mixed footage use screen-share analysis
  to protect demo work, then evaluate talking-head intervals separately. Inspect frames across
  the entire recording, including mode changes.
- Order `_intro` first, body clips naturally, `_outro` or `_outtro` last, case-insensitively.
  The script implements this and rejects competing intro/outro candidates.
- A prerecorded `endcard.mp4` passes through without analysis. Mark other pre-edited clips with
  `--passthrough /absolute/path.mp4`. Include only the intended ending, not every candidate.
- Work in `<project>/00_Project/edit/`; deliver `<project>/01_Footage/<name>_rough.mp4`.
  Without a scaffolded project, use `<source_dir>/rough-cut/<name>/` for both work and output.
  `/tmp` is for disposable experiments, never the only home of an edit or transcript.

## 1. Analyze once

Requires Python 3.9+, ffmpeg/ffprobe, and `mlx_whisper` for transcription. No Python packages
are needed by the script itself. Use the installed MLX CLI, not the unavailable `whisper` CLI.

```bash
python3 <skill>/scripts/pipeline.py analyze /absolute/part_intro.mp4 /absolute/part_01.mp4 \
  --mode screen-share --work /absolute/Project/00_Project/edit
```

This extracts mono audio directly from each original, batches uncached transcription in one MLX
process, caches word timestamps, detects silences,
and measures activity only inside relevant screen-share pauses. No full-video proxy is required.
The result is `analysis.json` plus `suggested-decisions.json`. Neither applies cuts automatically.
`--skip-transcript` is for timing tests or an explicitly silence-only pass, not retake editing.

Read [editing-rules.md](references/editing-rules.md) before deciding cuts. It consolidates the
speech protection, retake, noise, and activity rules from actual recordings.

Review the reported threshold and silence count. On screen-share, validate activity detection
against one known typing/scrolling interval before trusting a zero:

```bash
python3 <skill>/scripts/pipeline.py activity /absolute/source.mp4 --start 12 --end 16
```

Use `--threshold -35` only if inspection supports that setting; the default adapts to the audio.
The automatic threshold is a starting point, not a measured speech classifier.

## 2. Decide the edit

Copy suggestions to `decisions.json` on the first run; preserve and edit the existing decisions
on revisions. Read the transcript and candidate intervals together. Add confirmed retake cuts,
remove deliberate beats from suggestions, and protect active demo footage.

- Retakes are an editorial decision, scoped within each source clip. Keep the last complete
  genuine take, including the gap in the earlier-take cut. Never treat ordinary repeated demo
  narration as a retake. Record every group's timestamps and chosen take in the report.
- Inspect uncertain boundaries by listening to short source slices, not by re-transcribing
  the whole recording. Re-transcribe only windows that affect a proposed cut.
- Filler and cough removal are not implemented detectors in the script. Apply only confirmed
  events following the reference rules. Report “not analyzed” when no such pass was done.
- Put speed changes in `speeds` now, before graphics. Use them only where sped-up audio and
  screen work remain appropriate; do not accelerate an explanation.

The agent can review and render in the same turn. No additional approval is needed for a
reversible rough cut. Stop to ask only when a material editorial ambiguity cannot be resolved.

## 3. Build the shared timeline

```bash
python3 <skill>/scripts/pipeline.py build \
  --analysis /absolute/Project/00_Project/edit/analysis.json \
  --decisions /absolute/Project/00_Project/edit/decisions.json \
  --fps 30000/1001 --out /absolute/Project/00_Project/edit/edit.json
```

Use the intended sequence rate; the example is not a mandatory rate. The script merges
intersecting cuts, validates ranges, accounts for multiple clips and speed changes, and writes
`edit.json` plus `transcript.output.json`. Output intervals are quantized to whole frames.
Check `boundary_words_for_review` by listening; these words are not silently snapped or deleted
from the source audio. The transcript flags them because their ASR times cross edit boundaries.

[Timeline and CLI reference](references/pipeline.md) defines the decisions schema, caching,
timestamp mapping, supported inputs, and limitations. Never parse a generated filter graph to
recover the edit. Never hand-edit `edit.json`; change decisions and build again.

## 4. Render and verify

```bash
python3 <skill>/scripts/pipeline.py render \
  --manifest /absolute/Project/00_Project/edit/edit.json \
  --out /absolute/Project/01_Footage/example_rough.mp4
```

Hardware H.264 encoding is the default on Dan's Mac. Use `--encoder software` if hardware is
unavailable, and report the fallback. Rendering uses original footage at native dimensions,
normalizes output frame cadence, caches rendered source parts, and encodes final AAC once.
A revised first part does not force unchanged later parts to be rendered again.

Listen across retake seams, head/tail trims, uncertain word boundaries, and any noise cuts.
Watch screen-share cuts and source transitions. Probe duration, resolution, and frame rate
against the manifest. Synthetic checks do not establish good pacing on Dan's recordings.

Deliver the video and point to the manifest, mapped transcript, and decisions. Report original
and output duration, removed silences, resolved retakes, what needs review, and which optional
passes actually ran. Open the delivered file when useful.

## Improvement loop

`analysis.json` records analysis timing and cache hits; the output's `.render.json` records
render timings. For one representative raw/published pair, also track Dan's correction minutes,
clipped words, false retakes, and missed pauses. Compare cold runs, cached revisions, and human
correction time separately. Do not claim a speedup from synthetic tests or optimize removal %.
Historical evidence is in [history.md](references/history.md); update the current rule when a
lesson is accepted rather than appending a contradictory instruction to the main skill.
