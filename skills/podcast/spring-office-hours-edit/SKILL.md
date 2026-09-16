---
name: spring-office-hours-edit
description: >-
  Rough-edit a raw Spring Office Hours live stream recording down to the publish-ready podcast mp3.
  Cuts the 2 minutes of pre-show bumper music, lightly trims long silences while keeping the live
  conversational pacing, cuts right after the sign-off, normalizes loudness to the show's -14 LUFS,
  and delivers the mp3 plus an episode transcript. Use whenever Dan hands over a Spring Office
  Hours recording and says "podcast edit this", "cut this down to an mp3", "edit this episode",
  "rough edit the podcast", or "prep this for the podcast feed". This skill is specific to Spring
  Office Hours; other shows get their own skills. Do NOT use for YouTube video cuts
  (video-rough-cut), shorts (video-shorts), show notes (spring-office-hours-show-notes), or
  logging guest spots on other people's shows (podcast-appearance).
---

# Spring Office Hours: Episode Edit

Turn a raw episode recording into the publishable mp3. One pass: drop the pre-show bumper music,
trim only clearly dead air, cut after the sign-off, normalize loudness, encode mp3, and save a
transcript for the show-notes skill.

This is a live two-host conversation, not a scripted video. The pauses ARE the rhythm. When in
doubt, keep. The bar for cutting is "nobody would miss it", not "the pacing could be tighter".
There are no retakes on a live show, so there is no retake logic here. Fillers stay in.

## The show, measured (S5E18 benchmark, 2026-07)

These numbers come from comparing the raw S5E18 recording against the published mp3. They are
expectations to sanity-check against, not values to hard-code:

- The bumper music ran exactly 2:00. Speech started at 120.0s in the raw file.
- The published edit removed 127s total: the bumper plus about 7s of trailing chatter. It removed
  zero mid-show silences. Silence trimming here is a bonus Dan asked for, so stay light.
- The published episode is -14.3 LUFS integrated, LRA 10.8.
- Cold open: "Today is Monday, July 13th, 2026, and this is Spring Office Hours Season 5,
  Episode 18..."
- Sign-off: "...With that, I think that's the pod. We'll see you in the next one." The published
  cut ends right there. A trailing "See ya" and stream-stop noise were dropped.

If a run's numbers land far from these (a 5-minute "bumper", 40 minutes of trimmed silence),
suspect the detection before trusting the cut.

## Inputs

One recording, in order of preference:

1. **Audio-only download of the live stream** (m4a/mp3). Smallest and fastest. Dan downloads
   these into `/Users/vega/youtube/spring-office-hours/raw/`. When Dan names an episode without
   a path, look there first.
2. **Nothing but the episode token or a YouTube URL.** Fetch the audio directly:
   ```bash
   yt-dlp --no-warnings --flat-playlist --print "%(id)s | %(channel)s | %(title)s" \
     "ytsearch5:Spring Office Hours S5E18"   # pick the SpringDeveloper channel hit
   yt-dlp -f bestaudio -o "/tmp/soh-edit/$EP/source.m4a" "https://www.youtube.com/watch?v=<id>"
   ```
   (The channel has no /streams tab; search and filter on channel == SpringDeveloper.)
3. **The raw video file.** Episodes live in `/Users/vega/youtube/spring-office-hours/S5/` with
   the episode token in the filename (`S5E18`). Works fine, just 2GB heavier than it needs to be.

The pipeline is identical for all three; everything downstream is audio.

## Working directory

`/tmp/soh-edit/<episode>/` (e.g. `/tmp/soh-edit/S5E18/`). Create at start, leave artifacts
behind for cheap revisions.

## The script

`scripts/soh_audio.py` owns everything mechanical: extraction, transcription, the repetition
scan, RMS measurement, silence detection, the loudnorm passes, encoding, and the transcript
remap. It runs the same way every time, which is the point. What it deliberately does NOT do is
decide where the show starts and ends. It proposes, you confirm.

Every phase caches its artifacts in the work dir, so re-running after a nudged boundary costs
seconds.

## Step 1: Analyze

```bash
python3 <skill>/scripts/soh_audio.py analyze --ep $EP --src "$SRC"
```

Read the output before touching anything. Two lines decide whether you can continue:

- **"WHISPER REPETITION SUSPECTED"** means the transcript is degenerate somewhere. It shredded
  the entire sign-off region on S5E19. Re-transcribe from just before the first bad segment as a
  slice (that resets the conditioning) and use the slice for boundaries.
- **"NO sign-off formula"** on the END candidate. Sometimes correct and sometimes not. S5E20
  genuinely had no sign-off and ended on the guest goodbye; the fallback to last-sustained-speech
  was right. Confirm it in Step 2 rather than assuming either way.

The silence threshold is computed from the measured speech median, never hard-coded. Ignore
`silencedetect`; it reports zero silences on this show's audio at every usable threshold.

## Step 2: Verify both boundaries

Do not skip this, and do not render on an unverified boundary. The boundary cuts are the only
part of this edit that can quietly ruin the episode.

```bash
python3 <skill>/scripts/soh_audio.py verify --ep $EP --at <start>
python3 <skill>/scripts/soh_audio.py verify --ep $EP --at <end>
```

Whisper invents words inside music and inside end-of-file silence, so a candidate drawn from the
full-file pass proves nothing on its own. The slice re-transcription is independent evidence. If
it disagrees with the full-file transcript, or comes back empty, that candidate was debris: take
the next sustained run and verify that one.

Two judgment calls the script cannot make for you:

- A full-sentence reply after the sign-off ("Fantastic. Thanks, everyone.") is part of the
  sign-off. Keep it and end after it. A one-word tail ("See ya") is debris.
- If there is real post-show conversation, still cut at the sign-off, but say so in the report so
  restoring it is a one-line re-render.

## Step 3: Decide the trims

`analyze` lists every silence at or over 2s inside the show. That is a candidate list, not a cut
list, and the default answer is no.

| Silence | default |
|---|---|
| < 2s | keep, it is conversation |
| >= 2s | consider trimming to 0.75s |

Weight that table against the show. The published edits trim **zero** mid-show silences. A live
show has thinking pauses, screen-share pauses, and "let me pull that up" pauses, and they are the
rhythm. Nine seconds of nothing is dead air. Two and a half seconds after a punchline is the joke
landing, and cutting it makes the episode worse to save one second. When in doubt, keep, and say
in the report what you kept.

## Step 4: Render

```bash
python3 <skill>/scripts/soh_audio.py render --ep $EP --src "$SRC" \
  --start <confirmed start> --end <confirmed end> [--cut 993.96:996.27 ...]
```

Pass the confirmed **word** timestamps. The script applies the 0.5s lead-in and 1.0s tail pads,
collapses each `--cut` silence to 0.75s by keeping half the target on either side of the join,
builds the chain with atrim+concat via a filter script (never `aselect`, it desyncs), runs
loudnorm measure-then-apply, encodes 128k/44.1k stereo to match the feed, and remaps the
transcript onto the final timeline as `.srt` and `.txt`.

If you ever rework the span math, check the arithmetic and not just that it runs: an earlier
version centred the removal on the gap midpoint and padded outward across the join, which turned
a 2.31s pause into 1.86s instead of 0.75s. It rendered fine and trimmed almost nothing.

On loudness: expect about -14.5 LUFS, not -14.0. Dan's source peaks above digital zero, so
reaching the target would need gain that breaks the -1.5 dBTP ceiling and loudnorm falls back to
dynamic mode. The script says so when it happens. That is the ceiling talking, not a defect, and
no number of passes changes it.

## Step 5: Deliver + report

The script writes the mp3, `.srt` and `.txt` into
`/Users/vega/youtube/spring-office-hours/exports/` and refuses to overwrite an existing
`$EP.mp3`, since that would be a published episode. If it reports saving `$EP-new.mp3`, stop and
tell Dan rather than quietly delivering the wrong file. Then `open -R` the mp3.

Keep the working dir. "Start it 10 seconds earlier" or "put back the pause at 41:22" is a
re-render of a few seconds, because analyze and the transcript are cached.

Report so Dan can verify the boundaries without listening to the episode:

```
Original: 1h 06m 56s → Episode: 54m 10s
Show starts 2:00.3: "Today is Monday, July 13th, 2026, and this is Spring Office Hours..."
Show ends 1h 05m 02s: "...I think that's the pod. We'll see you in the next one."
Bumper cut: 2m 00s · End clipped: 7s · Silences trimmed: 3 (longest 6s at 41:22)
```

Always quote the detected first and last lines. The boundary cuts are the biggest risk in this
skill, and the quotes make a wrong boundary obvious at a glance. Say what you deliberately kept
too: a trim candidate you left in is a decision Dan should get to see.

Then offer the next step: `spring-office-hours-show-notes` can build the description and links
from the transcript now on disk. When both are wanted, `spring-office-hours-prep` runs the pair.

## Pitfalls log

Append a dated line every time a run burns you. Seeded with lessons inherited from
video-rough-cut:

- (seed) `whisper` CLI is not installed on this machine. Use `mlx_whisper` (miniforge, on PATH).
- (seed) `aselect` desyncs audio on cuts. Always atrim+concat via a filter script.
- (seed) The noise-floor+6dB threshold under-detects on Dan's bimodal setup. Detect about 15dB
  below the speech median (-35dB has worked).
- (seed) Whisper hallucinates sentences inside detected silence, especially at end of file.
  Cross-check boundary lines against the silence list before trusting them.
- (seed) Whisper invents lyrics/phrases during bumper music. Verify the show-start candidate
  with a slice re-transcription before cutting.
- (seed) Always pass `-nostdin` to ffmpeg inside shell read loops. It eats stdin and mangles the
  next line's timestamps.
- (2026-07-27, S5E19) whisper small.en fell into a repetition loop ("I'm going to say, ..." x100)
  for the final ~6.5 minutes of the full-file pass, mangling the sign-off region. Scan the
  transcript for degenerate repeats; if found, re-transcribe from just before the first bad
  segment as a slice (resets the conditioning) and splice it in for boundaries and deliverables.
- (2026-07-27, S5E19) Single-pass loudnorm landed -14.6 LUFS against the -14 target (S5E18
  benchmark is -14.3). Close enough for the feed, but two-pass loudnorm (measure, then feed
  measured_* values) would hit -14.0 if a run lands further off.
  **Superseded 2026-08-17, see below: two-pass is not the fix.**
- (2026-08-17, S5E20) Two-pass loudnorm also landed -14.6, identical to single-pass. The pass-1
  JSON explains it: `normalization_type: dynamic`. Dan's source peaks above digital zero
  (input_tp was +0.63 dBFS), so reaching -14.0 needs upward gain that breaks the TP=-1.5 ceiling,
  and loudnorm falls back to dynamic. The binding constraint is true peak, not pass count. Do not
  burn a second pass chasing -14.0. Accept -14.5ish, or raise TP if Dan ever wants it hotter.
- (2026-08-17, S5E20) `silencedetect` reported ZERO silences at every threshold from -30dB to
  -50dB, even at d=0.5s, on a file that has 4016 quiet runs at -35dB. It is unreliable here.
  Measure windowed RMS instead (astats with reset=1, print RMS_level per frame), then scan the
  chronological values for runs below threshold. That also gives the speech median for free, so
  it replaces the separate calibration step. Zero detections is the tell.
- (2026-08-17, S5E20) Not every episode has the formulaic sign-off. S5E20 has no "that's the pod"
  and no replay mention; it ends on the guest thank-you and "All right, have a good one." When
  the formula is missing, do not keep scanning backwards for it. Take the last real speech run,
  confirm it with a tail slice re-transcription, and end 1.0s after.
- (2026-08-17) Silence-trim arithmetic is easy to get wrong in a way that still renders cleanly.
  The first version of `keep_spans` centred the removal on the gap midpoint AND padded outward
  across the join; on a 2.31s pause targeting 0.75s it removed 0.45s and left 1.86s. No error, no
  desync, just a trim that did nothing. To collapse silence [a,b] to D, keep up to `a + D/2` and
  resume at `b - D/2`. When changing this, assert on the numbers (removed seconds, pause left in
  the output), not on whether ffmpeg exited 0.
- (2026-09-14, S5E22) The repetition scan printed "clean" while whisper looped on "You can go to
  the website" for ~60s of the outro (3812-3872s) and swallowed the real sign-off. The loop was
  split into segments that differed by a word, so identical-segment counting never fired. Two
  cheap checks caught it: word rate over ~6 words/sec (the loop hit 128; real fast talk tops out
  near 7) and any 5-gram repeated 3+ times within 60 words. Both also flag natural repetition
  ("Do you want to work at X? Do you want to work at Y?"), so confirm each hit with a fresh slice.
  The fix was the usual slice-and-splice from a clean segment boundary before the loop, with
  `--condition-on-previous-text False` (slightly better text than the default). Run both checks
  every time, whatever the scan prints.
- (2026-09-14, S5E22) The live-from-KCDC episode broke the studio template three ways, all fine
  once verified. The bumper ran ~1:25, not 2:00 (speech at 91.9s). The cold open began "We did
  it!" before "Today is...". The outro matched no sign-off formula ("I think this is a fantastic
  episode... Thanks everyone"). Room noise also meant zero silences >= 2s, so nothing to trim.
  Expect all of this on any on-location episode.

## What this skill does NOT do

- Video deliverables of any kind. That is video-rough-cut.
- Show notes, titles, or descriptions. That is spring-office-hours-show-notes.
- Uploading to Transistor or anywhere else.

One job: raw episode in, publishable mp3 and transcript out, fast.
