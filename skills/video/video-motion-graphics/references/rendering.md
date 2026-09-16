# Rendering, previews, and delivery

Requires Node, ffmpeg/ffprobe, and system Chrome. Install once in the skill's `scripts/` folder:
`PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm ci`. Reuse the installed dependencies thereafter.

## Template parameters

- lower-third: `name`, `role`
- section-title: `num`, `title`, `kicker`, `side`
- callout: `label`, `value`, `side`
- subscribe-nudge: `channel`, `side`
- spotlight: fractional `x`, `y`, `w`, `h` plus `label`, `dim`

Pass `side: "right"` only when the real frame supports it. Keep the default card placement in
bottom corners. Measure spotlight fractions against a real source frame. Long URLs and titles
can overflow: shorten display copy or adapt layout before rendering the sequence.

## Poster, then motion

```bash
node <skill>/scripts/render.mjs --template <skill>/assets/templates/lower-third.html \
  --params-file /absolute/params.json --duration 6 --fps 30000/1001 --scale 2 \
  --poster /absolute/poster.png --at 2.2

node <skill>/scripts/render.mjs --template <skill>/assets/templates/lower-third.html \
  --params-file /absolute/params.json --duration 6 --fps 30000/1001 --scale 2 \
  --out /absolute/cache/lower-third --mov /absolute/overlays/lower-third.mov
```

Match the actual sequence FPS and dimensions, not the example. Decimal (`29.97`) and fractional
(`30000/1001`) rates are accepted. The same rate controls `seek()` times and FFmpeg encoding.
`render.json` records frame count and actual encoded duration. `--width` and `--height` set the
CSS viewport for templates designed for that layout; ordinary cards remain 1920×1080 CSS pixels.

Unchanged template/parameters/dimensions/rate/duration/browser reuse existing frames and MOV.
A shortened revision removes stale renderer-owned PNGs and explicitly bounds encoding by frame
count. Cache directories are exclusive to a single render job. `--no-cache` forces new frames.
Use repeated `--dependency /absolute/asset` for local images or other files whose content changes;
self-contained templates need none. After changing installed fonts, use `--no-cache`. Remote,
mutable dependencies are unsuitable for cached final work: vendor them or disable cache.
Waits use actual font/image readiness, not a guessed sleep. Templates must implement both APIs.

## Graphics plan

All paths are absolute. All placement times are on the BASE VIDEO's clock. Generate
`video_identity` using Python `Path(video).stat()`; store `st_size` and `st_mtime_ns`. A changed
base or manifest invalidates the plan until placements are checked. Omit both manifest fields
only for footage whose transcript was made directly from that same base video.

```json
{
  "video": "/absolute/Project/01_Footage/example_rough.mp4",
  "video_identity": {"size": 123456, "mtime_ns": 123456789},
  "edit_manifest": "/absolute/Project/00_Project/edit/edit.json",
  "manifest_id": "copy-id-from-edit.json",
  "clips": [{
    "asset": "/absolute/Project/03_Graphics/overlays/name.mov",
    "start": 31.4,
    "duration": 6.0,
    "anchor": "Dan Vega at output 33.2s",
    "purpose": "Introduce the speaker"
  }]
}
```

The composite script supports full-canvas PNGs, ProRes alpha MOVs, and full-frame video inserts.
Asset raster dimensions must match the base video. VP9 alpha inputs use the libvpx decoder.
Later plan entries paint over earlier entries where they overlap; avoid accidental overlaps.
It keeps narration from the base video and does not mix asset audio. For inserts, author their
visuals against that narration. Speed changes and camera transformations happen before this
compositor; this tool does not implement an editing timeline with arbitrary tracks or transitions.

```bash
# A short, lower-resolution preview around the graphic, with the real surrounding narration.
python3 <skill>/scripts/composite.py --plan /absolute/graphics.json \
  --start 29 --duration 12 --width 960 --out /absolute/preview.mp4

# After preview checks, the full native-size composite.
python3 <skill>/scripts/composite.py --plan /absolute/graphics.json --out /absolute/example_gfx.mp4
```

Previews can begin mid-overlay: the script seeks that asset too, retaining its animation phase.
Intervals and looped stills are bounded; assets are trimmed to their scheduled duration. A preview
scales base and overlays together; final renders retain native size. Default encoding is hardware
H.264 on Mac, with explicit `--encoder software` fallback. The script verifies output duration;
watch and listen to assess design and sync.

## Alpha and code assets

H.264 does not preserve alpha. Use ProRes 4444 (`yuva444p10le`) for transparent Premiere masters.
VP9/WebM requires the libvpx decoder when compositing with FFmpeg; the native decoder can lose
alpha. The compositor selects it for VP9 inputs. Check a new alpha asset over a saturated ground
before delivery. Prefer one delivery format per use: MP4 insert or MOV overlay, with an additional
format only when the edit needs it. Do not use `backdrop-filter` for captured transparency.

## Validation

Run `node --test <skill>/scripts/render-options.test.mjs` for numeric checks. The separate
`test_media.py` renders tiny real fixtures to test rational rates, stale-frame removal, cache
reuse, and preview placement; it needs Chrome, Playwright, Python, and FFmpeg. It does not judge
visual taste. Representative new templates still need real-frame and motion review.
