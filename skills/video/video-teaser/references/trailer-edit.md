# Trailer timeline and rendering

Requires Python 3.9+, ffmpeg/ffprobe. For title/caption assets, use the installed
`video-motion-graphics/scripts/render.mjs` (Node, Playwright, system Chrome). The montage script
itself uses only Python's standard library. All media is local and all paths must be absolute.

## Plan schema

This is an illustrative layout, not a valid plan until real sources, times, and durations are set.
`shots` are in final picture order. `audio` has independent output placements, enabling dialogue
to begin before a picture cut or continue across several shots. Original audio in picture shots
is muted; add desired dialogue or source effects explicitly as audio tracks.

```json
{
  "fps": "30000/1001",
  "width": 1920,
  "height": 1080,
  "shots": [
    {"asset": "/absolute/problem-demo.mp4", "source_start": 12.0, "duration": 3.0, "purpose": "Show the problem"},
    {"asset": "/absolute/dan-wip.mp4", "source_start": 42.0, "duration": 4.0, "purpose": "The central question"},
    {"asset": "/absolute/real-result.mp4", "source_start": 5.0, "duration": 3.0, "purpose": "Glimpse of proof"},
    {"asset": "/absolute/title-card.mp4", "source_start": 0.0, "duration": 3.0, "purpose": "Promise and coming soon"}
  ],
  "audio": [
    {"role": "dialogue", "asset": "/absolute/dan-wip.mp4", "source_start": 40.0,
     "start": 1.0, "duration": 6.0, "gain_db": 0, "transcript": "/absolute/dan-wip-transcript.json"},
    {"role": "music", "asset": "/absolute/cleared-track.wav", "source_start": 0.0,
     "start": 0.0, "duration": 13.0, "gain_db": -18, "fade_in": 0.1, "fade_out": 1.0}
  ]
}
```

Times in `source_start` and transcripts are on the respective media file's clock. `start` on
an audio item is on the trailer output clock. Keep audio duration within its actual source and
the trailer. Include a source-clock transcript for each dialogue excerpt if caption mapping is
needed. A word crossing an excerpt boundary is flagged for listening rather than silently snapped.

Shots quantize to whole frames. The `.render.json` receipt records actual output shot times; use
those if a planned visual/sound cue needs frame-exact alignment. Audio starts quantize to ms.
Do not casually repeat or reorder dialogue: verify that the resulting meaning remains authentic.

## Assets

`assets/title-card.html` takes `kicker`, `title`, and `subline`. Keep the title to a few words
or two short lines; use `\n` in JSON for an intentional break. For example a specific question
followed by the real title later, not generic “Everything changes” hype.

```bash
node <graphics-skill>/scripts/render.mjs --template <teaser-skill>/assets/title-card.html \
  --params-file /absolute/title.json --duration 3 --fps 30000/1001 \
  --poster /absolute/title-poster.png --at 1

node <graphics-skill>/scripts/render.mjs --template <teaser-skill>/assets/title-card.html \
  --params-file /absolute/title.json --duration 3 --fps 30000/1001 --out /absolute/cache/title

ffmpeg -nostdin -y -framerate 30000/1001 -i /absolute/cache/title/f_%04d.png \
  -c:v h264_videotoolbox -b:v 12M -pix_fmt yuv420p /absolute/title-card.mp4
```

A PNG can also be a held shot. All shots are fit inside the output frame with padding; this
preserves code instead of cropping it. Prepare deliberate crops/zooms separately when needed.
Opaque rendered inserts belong in the shot list; an alpha MOV belongs over footage in the
shared graphics compositor. Do not treat a transparent overlay as full-frame B-roll.

## Render

```bash
python3 <teaser-skill>/scripts/montage.py --plan /absolute/trailer-plan.json \
  --out /absolute/Project/04_Exports/teaser/example_teaser.mp4
```

For a short creative preview, save a separate plan containing the chosen sequence and adjust
its audio placements to that preview's clock. Use smaller output dimensions if useful. Reuse
that direction in the final plan. The script caches each rendered visual shot by source identity,
trim, raster, rate, encoder, and FFmpeg version; it remixes audio on revisions. Use
`--encoder software` for environments without Mac hardware encoding. No concurrent writers to
the same plan/cache/output. Sources must stay immutable; replace a WIP export only after checking
and updating its source anchors.

Dialogue gets an 8 ms fade-in and 35 ms fade-out by default to remove hard sample edges.
`fade_in` and `fade_out` override them in seconds for any role. Preserve source handles around
syllables; fades cannot repair a clipped word, and long fades can swallow consonants.

Music defaults to `duck_db: -12`, `duck_attack: 0.18`, and `duck_release: 0.65`. These sample-level
cosine ramps start before speech and recover gradually after it; overlapping dialogue uses the
deepest envelope rather than multiplying duck levels. Use a shallower duck or longer release
when the pulse should carry across short sentence gaps. Avoid abrupt amplitude gates in the
underlying score, too. Final audio is normalized toward -14 LUFS with a -1.5 dB true-peak target
and exported at 48 kHz. Numerical checks and ASR do not prove a smooth subjective mix; report
listening limits honestly and listen on ordinary speakers when playback is available.

## Captions

The montage emits `<output-stem>.transcript.json` on the teaser clock. Group its words into short
phrase cues, preserving punctuation and natural pauses. Keep the words accurate; title-card
copy is a separate editorial layer. Validate cues against the actual mixed dialogue.

`assets/captions.html` parameters:

```json
{"bottom": 85, "cues": [{"start": 1.0, "end": 3.2, "text": "A short, accurate phrase."}]}
```

Render a transparent ProRes MOV for the trailer duration using the graphics renderer, then add
it at output 0 via `video-motion-graphics/scripts/composite.py`. Use the trailer's actual rate
and dimensions; there is no source-to-rough-cut map at this stage. Keep captions off a title card
when they duplicate it, but do not hide essential narration on sound-off viewing. Inspect feed-size
readability and any collision with screen text.

## Verification

`python3 -m unittest discover -s <teaser-skill>/scripts -p 'test_*.py' -v` exercises real tiny
media: shot order, audio placements, word mapping, and cache reuse. It does not prove a compelling
trailer. Watch the actual trailer with sound and muted, including all edits and the final title.
