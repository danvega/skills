# Shared timeline and pipeline CLI

Requires Python 3.9+, ffmpeg/ffprobe, and (unless skipped) the installed `mlx_whisper` CLI.
`python3 scripts/pipeline.py --help` lists commands. Run tests with:

```bash
python3 -m unittest discover -s <skill>/scripts -p 'test_*.py' -v
```

## Files

- `analysis.json`: ordered source identities, probes, transcript locations, silence candidates,
  screen activity rates, notes, and timings.
- `suggested-decisions.json`: regenerable silence suggestions. Copy to `decisions.json` and
  review before building. Analysis never overwrites your reviewed decisions.
- `edit.json`: generated shared manifest, including sources, decisions, frame rate, and each
  kept interval's source/output times, speed, and frame count.
- `transcript.output.json`: words mapped onto the edit clock, with source provenance. Removed
  words and partially cut words are separate lists. Output words keep the Whisper `segments`
  shape so `video-shorts/scripts/extract_words.py` can read them without `--filter`.
- `cache/`: extracted audio, transcripts, analyses, filter graphs, and rendered source parts.
  These are project-local, regenerable artifacts. Never check them into the skills repository.

## Transcript-only reuse

For shorts, teasers, or social copy needing the exact export's transcript without an edit pass:

```bash
python3 <skill>/scripts/pipeline.py transcribe /absolute/final.mp4 \
  --work /absolute/Project/05_Transcripts/final
```

`transcripts.json` lists source identities and the actual per-source transcript path. Audio is
extracted directly. Uncached inputs are passed to MLX together in one process, with unique
basenames, and completed transcripts are promoted from a temporary output directory. Repeated
runs reuse matching transcripts. The analyze command uses the same preparation and batch cache.

## Reviewed decisions

Use the exact clip IDs from analysis. Include every clip once, even those with no edits.
All times here are seconds on that clip's source clock. Cut boundaries are final, already padded.
Reasons are free text; retain them so the edit can be explained and reversed.

```json
{
  "clips": [{
    "id": "copy-id-from-analysis",
    "cuts": [{"start": 12.4, "end": 15.8, "reason": "earlier retake, keep 15.8s take"}],
    "speeds": [{"start": 30.0, "end": 36.0, "speed": 2.0, "reason": "silent boilerplate"}]
  }]
}
```

Intersecting cuts are merged. Speed intervals cannot overlap; they can span a cut, and only
surviving material gets sped up. Each output interval rounds to whole frames at the chosen rate.
Rendering uses the same frame counts, pads/trims audio to the corresponding duration, and
normalizes output cadence. Small rounding differences are limited to about a frame per interval
and represented in subsequent output offsets. Timing within a surviving interval maps as:

`output_start + (source_time - source_start) / speed`, clamped to the interval's output end.

A manifest ID changes when the edit changes. Graphics plans must store that ID; invalidate their
placements if it no longer matches. A final Premiere export has its own timeline: transcribe that
export for shorts, never reuse the intermediate's mapped transcript without an actual final map.

## Map an anchor

Prefer the output-clock transcript directly. For a source-clock anchor:

```bash
python3 <skill>/scripts/pipeline.py map --manifest /absolute/edit.json \
  --clip exact-clip-id --time 42.3
```

Returns a time or `null` for removed material. Only after listening and confirming that the word
survived may you retry with `--snap 0.15` (maximum 0.3 s). Snaps are marked in the result.
Never snap a distant removed phrase to a surviving edge. Missing maps do not mean clocks match.
For legacy cuts with no manifest, reconstruct and verify a map from existing cut evidence or
transcribe the delivered cut directly. Do not rerender a working legacy cut just to obtain JSON.

## Cache and performance

Source identity uses absolute path, size, and nanosecond modification time. This avoids hashing
multi-gigabyte recordings on every run. Keep sources immutable; deliberately replacing bytes
while preserving size and mtime requires removing that source's cache and reanalyzing. Different
files with the same basename do not collide. ASR caches also include model/settings; analysis
caches include threshold and mode. Renders include source identity, intervals, rate, encoder,
and FFmpeg version. Revisions only rerender changed source parts; final remux/audio encode still runs.

Do not run concurrent writers against the same work directory, frame directory, or output path.
Interruptions leave `.partial` files; only completed artifacts are reused. Cache storage can be
large, particularly the PCM-audio render intermediates. Remove regenerable cache when a project
is finished, retaining the transcript files it references or copying them and updating the project
records before cleanup. Keep edit decisions and source footage.

No total runtime target has been validated on real footage. Analysis and render receipts report
wall time and cache hits; compare the same sources/settings on cold and warm runs.

## Supported media and boundaries

Native even dimensions, square pixels, unrotated footage, one primary video and zero or one
primary audio stream. The first audio stream is used. Other tracks are not mixed. Explicitly
prepare a source mix if a recording has separate microphone/desktop tracks. All clips must have
the same dimensions for concatenation; choose and normalize the intended sequence before analysis
when they differ. Clips without audio receive silence in the render. Audio/video start offsets
over 50 ms are rejected for explicit normalization instead of quietly losing sync.

The renderer normalizes output to the chosen constant frame rate at render time, including VFR
sources. Verify seams and sync on unusual recordings. It produces SDR 8-bit H.264; HDR/color-managed
work needs a deliberate separate workflow. Hardware encoding is the Mac default; software fallback
is explicit. The script does not automatically detect retakes, fillers, or coughs, and candidates
still require editorial review. Source footage is never overwritten.
