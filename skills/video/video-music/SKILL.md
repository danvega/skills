---
name: video-music
description: >-
  Add a background music bed to an edit: pick an instrumental track from Epidemic Sound that
  fits the channel's taste, have Epidemic recut it to the video's exact length, and mix it quiet
  and ducked under Dan's voice. Mixes it into the preview and puts it on its own stereo track pair
  in the Premiere XML. Use when Dan asks for background music, a music bed, "add some music", or
  a different track, or when the video-edit orchestrator reaches the music stage. Music is
  optional: only add it when Dan wants it for this video. Needs an approved rough cut. Not for
  sound effects (video-sfx).
---

# Background music

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

The bed is one track for the whole video. Epidemic Sound recuts it to the exact length, so it
keeps its real intro and ending instead of being chopped. `vedit music` brings it to a quiet
level, fades it in and out, and ducks it under Dan's voice. Levels and ducking are in
`style/style.json` under `music` (the bed lands about 20 dB under the voice).

## 1. Length and taste

```bash
$V music --work WORK
```

Prints `target_ms` (the cut's length) and the brand's `music` block: `mood`, `searches`, `bpm`,
and `approved` tracks Dan liked before. If `mood` is null, ask Dan what he wants for this
channel. Save his answer in `style/brands/<brand>.json` so the next video does not ask again.

## 2. Pick a track

With the Epidemic Sound MCP:

1. `SearchRecordings` with each of the brand's `searches` (or terms from his mood), filter
   `vocals: false`, and the brand's `bpm` range if set. Ask for about 8 results.
2. Pick the best fit: instrumental, steady, nothing that fights speech (no busy leads, no big
   drops). If an `approved` track still fits, it is a safe choice.
3. Tell Dan the pick (title, artist) and one or two runners-up in a line each.

## 3. Recut and download

1. `EditRecording` with the recording id and
   `{"targetDurationMs": TARGET_MS, "downloadAudioFormat": "WAV", "forceDuration": true,
   "skipStems": true, "maxResults": 1}`.
2. `PollEditRecordingJob` with the job id until `COMPLETED`.
3. `DownloadRecordingEdit` with `{"jobId": ..., "editId": ...}`, then download its `assetUrl`:
   `curl -sSf -o WORK/music/source.wav "ASSET_URL"`.

## 4. Build

```bash
$V music --work WORK --source WORK/music/source.wav --id ID --title "TITLE" --artist "ARTIST"
$V preview --work WORK
```

Writes `WORK/music/bed.wav` and `WORK/cues/music.json`. The preview mixes it in. Its checks listen
to the dialogue alone, so music cannot hide a cut problem. Then `$V export` puts the bed on its
own stereo track pair (A3), named for the song, in the `02_Audio/Music` bin.

## Check

Report the bed's loudness (`bed_lufs` in the output) and the dialogue's. The bed should sit about
20 dB under the voice. If Dan says it is too loud or quiet, change `lufs` under `music` in
`style.json` and build again.

## When the cut changes

The bed is built for one cut. If the cut list changes, `preview` and `export` stop with "built
for an older cut". Run steps 1, 3, and 4 again with the same track: the length changed, so
Epidemic recuts it again.

## Gotchas

- (2026-10-07) The first bed at −31 LUFS with heavy ducking came out at −41.5 LUFS and was
  inaudible. −29 LUFS with a gentle duck (threshold 0.06, ratio 2) gives a bed about 20 dB under
  the voice that ducks about 6 dB while Dan talks.
- (2026-10-07) The Epidemic download URL expires. Download right after `DownloadRecordingEdit`.
