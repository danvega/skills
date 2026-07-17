---
name: rough-cut
description: >-
  Produce a rough cut of a raw YouTube recording — trim dead air, remove filler words, and resolve
  retakes while preserving natural pacing. Handles both talking-head and screen-share footage; the
  output is a first pass to finish in an editor, not a final render. Use when Dan drops a video file
  and says "rough cut this", "first pass on this", "trim the silences", "cut the dead air", "remove
  the ums", "remove the duplicates", "I re-recorded some parts", or "clean up this recording". Do
  NOT use for titles/thumbnails (video-packaging), extracting short clips, captions, zooms, or
  b-roll.
---

# Rough Cut

Turn a raw recording into a rough cut: dead air trimmed, fillers gone, retakes resolved. The goal
is a watchable first pass that's safe to hand to an editor — **when in doubt, keep it**. A missed
pause costs seconds in the edit; a clipped word costs a re-render and trust.

## Inputs

- Video file path (ask if not given).
- Footage mode: `talking-head` or `screen-share`. Ask if not obvious from the filename or context —
  the modes cut differently (see Step 3).

## Working directory

`/tmp/rough-cut/<basename>/` — create at start, leave artifacts behind for cheap revisions.

## Step 1 — Analysis proxy + audio

Make a 1080p working copy for the *analysis* steps (transcription, silence detection, scene
checks) — it keeps them fast. The proxy is never the deliverable: the final render (Step 4) cuts
the original source at its native resolution, so a 4K recording stays 4K.

```bash
ffmpeg -y -hwaccel videotoolbox -i "$SRC" \
  -vf scale=-2:1080 \
  -c:v libx264 -preset fast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k /tmp/rough-cut/$NAME/proxy.mp4
ffmpeg -y -i /tmp/rough-cut/$NAME/proxy.mp4 -vn -ac 1 -ar 16000 /tmp/rough-cut/$NAME/audio.wav
```

`-hwaccel videotoolbox` matters: HEVC software decode turns 30 seconds into 5 minutes on 4K
sources. `scale=-2:1080` is orientation-proof.

## Step 2 — Transcript

```bash
whisper /tmp/rough-cut/$NAME/audio.wav \
  --model small.en --word_timestamps True --output_format json \
  --output_dir /tmp/rough-cut/$NAME --language en
```

Use `small.en`, not `tiny.en` — tiny drops words and collapses repeated lines, which hides exactly
the retakes this skill needs to find. Two known limits shape everything downstream:

- Whisper word times are ±100–300ms. Fine for a rough cut **if you pad generously** (Step 4).
- Whisper hides pauses *inside* word durations. A "word" lasting 2s+ is really word-plus-pause (or
  a swallowed retake). Treat every stretched word as a suspect region: re-transcribe a ±3s window
  around it (`ffmpeg -ss <t-3> -t 6` + whisper on the slice) before cutting near it.

## Step 3 — Build the cut list (conservative by design)

### Silences

Calibrate the threshold to the recording, never hard-code one: measure per-window RMS, take the
10th percentile as the noise floor `F`, and detect at `F + 6dB`:

```bash
ffmpeg -i proxy.mp4 -af silencedetect=noise=${THRESH}dB:d=0.6 -f null - 2>&1 | grep silence_
```

| Silence | talking-head | screen-share |
|---|---|---|
| < 0.6s | keep | keep |
| 0.6–2s | trim to 0.4s | keep |
| > 2s | trim to 0.5s | see activity check |

**Screen-share activity check:** on a screencast, silence while the screen is *changing* is
content — typing, scrolling, a build running. Only cut a long silence when the frame is also
static. Sample scene-change scores inside the window:

```bash
ffmpeg -ss $START -t $DUR -i proxy.mp4 \
  -vf "select='gt(scene,0.003)',metadata=print" -f null - 2>&1 | grep -c scene_score
```

Zero or near-zero changes + silence → dead air, trim to 0.7s. Anything happening on screen → keep
and list it in the report instead.

### Fillers

Cut standalone `um`, `uh`, `er`, `hmm` with 50ms padding. Leave hedges ("so", "you know", "I
mean", "basically") alone in v1 — cutting those changes the delivery, and that's an editing
decision, not a rough-cut decision.

### Retakes / duplicates

Dan's recording pattern: say a line, decide it wasn't right, and re-record it — so duplicated
content is the norm, not the exception, and **the later take is the correct one by definition**
(he re-recorded *because* the first was wrong). Always keep the last take of a duplicate group
and drop every earlier one; never keep both.

- Detect by fuzzy-matching sentence openers (first 3–5 words) and 4-gram overlap (similarity
  > 0.7) across a **60-second window** — retakes restart the line, they rarely repeat it
  verbatim. A retake boundary is usually preceded by a long pause or a slate phrase ("okay",
  "again", "take two", "let me try that again").
- Drop the earlier take **and the gap** between takes as one cut.
- The only exception worth flagging: if the last take ends mid-sentence (he got interrupted, the
  recording stopped), don't silently keep a broken take — keep the previous complete one and call
  it out in the report.
- List every group in the report (`line → takes at [t1, t2] → keeping t2`) so an override is one
  sentence away.

### Never cut

- Laughs and reactions — whisper writes them as silence. Before cutting any silence, check its
  RMS against the noise floor: above `F + 10dB` means audible content, keep it.
- Deliberate beats — the pause after "and here's the thing…". If a silence directly follows a
  question or an emphasis word, trim it no shorter than 0.5s.

## Step 4 — Report, then render

Print the summary and render in the same turn — the render is non-destructive and revisions are
cheap:

```
Original: 14m 20s → Rough cut: 11m 05s (23% removed)
Silences trimmed: 41 · Fillers cut: 18 · Retake groups resolved: 3 (listed above)
Kept for review: 2 long silences with screen activity (6:12 build, 9:48 scrolling)
```

Pad every keep boundary: **0.15s before word onsets, 0.15s after word ends.** Rough-cut padding is
deliberately loose — whisper's timing error must land inside the pad, never inside a word.

Render with trim+concat, **not** the `select` filter (select desyncs audio). One trim/atrim pair
per keep interval, written to a file. **Cut the original source, not the proxy** — the timestamps
transfer 1:1 (the proxy is a straight transcode), and the output keeps the source's native
resolution. Never downscale:

```bash
ffmpeg -y -hwaccel videotoolbox -i "$SRC" \
  -filter_complex_script filter.txt \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset fast -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k \
  /tmp/rough-cut/$NAME/rough.mp4
```

On 4K/HEVC sources libx264 gets slow — `-c:v h264_videotoolbox -b:v 30M` renders minutes faster
at quality that's fine for a cut that gets edited further. If ffprobe shows the source is VFR
(variable frame rate — some phone/DJI footage), normalize it to a CFR mezzanine at native
resolution first and cut that instead; VFR timing can drift against times measured on the proxy.

## Step 5 — Deliver

- Save to `<source_dir>/rough-cut/<source_name>_rough.mp4` and `open` it.
- Keep the working dir: "put back the pause at 6:12" or "use take 1 instead" is a seconds-fast
  re-render, not a redo.

## Calibration — TODO (do this before trusting the targets)

The silence table above is a starting guess. Calibrate it against real style: take one raw
recording and its published cut, measure what the edit actually removed (compression %, shortest
kept pause, how retakes were resolved), and replace the table and the target compression with
measured numbers. Add the video's name here as the benchmark reference.

## Pitfalls log

Append a dated line here every time a run burns you — this log is where the skill earns its keep.

- (seed) `select`/`aselect` desyncs audio on cuts — always trim+concat.
- (seed) `tiny.en` drops words and collapses retakes — `small.en` minimum.
- (seed) A whisper "word" spanning 2s+ hides a pause or a retake inside it — re-window before
  cutting near it.
- 2026-07-16: `whisper` CLI isn't installed on this machine — use `mlx_whisper` (miniforge, on
  PATH) with `--model mlx-community/whisper-small.en-mlx --word-timestamps True`; same JSON output.
- 2026-07-16: the screen-share activity check silently reports 0 scene changes if you pass
  `-v error` — `metadata=print` writes at info level, so `-v error` swallows it and every window
  looks static. Omit `-v error` (or use `-v info`) on the scene-change count; keep `-v error`
  elsewhere. Sanity-check the mechanism against a known-active window before trusting a 0.
- 2026-07-16: Dan edits in a **3840x2160** Premiere sequence, so the 1080p-proxy render drops in
  upscaled 200%. Detect against the proxy (fast), but render the **final deliverable from the
  original source at native resolution** — reuse the same `filter.txt` (cut timestamps are
  resolution-independent), point `-i` at the source, drop the `scale`, and encode 4K with
  `-c:v h264_videotoolbox -b:v 50M -maxrate 60M -bufsize 80M` (libx264 at 4K is far slower).

## What this skill does NOT do

- Zooms, captions, b-roll, music, or any finishing — that's the editor pass.
- Short-form clip extraction or repackaging.
- Uploading anywhere.

One job: raw recording in, safe rough cut out, fast.
