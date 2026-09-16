---
name: video-teaser
description: Cut a short pre-release teaser clip from an IN-PROGRESS video and write the tweet options to promote it before the video is published. Use whenever Dan wants to tease, trail, or preview a video that is not out yet — "make a teaser", "cut a trailer", "sneak peek", "tease this video", "build some hype", "coming soon post", "promote this before it's published" — even if he only says he wants to tweet about a video he is still working on. Runs on whatever footage exists NOW (a preview/rough export in 04_Exports, or raw recordings in 01_Footage); it never waits for the final export. Promotion of an already-published video on X is video-x-clips, NOT this; 9:16 Shorts from the final export are video-shorts. Output is one captioned teaser mp4 plus 2-3 ready-to-paste tweet options with deliberately vague timing, delivered as files only — nothing goes to the ContentOS shorts board or social calendar.
---

# Video Teaser

Cut one short teaser from a video that is still being made, plus the tweet to post with it.
A teaser's job is the opposite of an X clip's: an X clip delivers a complete mini-argument;
a teaser **opens a loop and refuses to close it**. Success is "I want to see that" replies,
bookmarks, and profile follows. The viewer should leave knowing what question the video
answers and NOT knowing the answer.

This runs pre-publish by design. Do not wait for, or ask for, the final export. Do not
apply the video-x-clips/video-shorts rule that clips must match the published video — a
teaser is promotion for something that doesn't exist yet, so a preview cut is exactly right.

## Inputs

Source priority (announce which one you used):

1. **A preview or rough export** in `/Users/vega/youtube/<Project>/04_Exports/` (filenames
   containing Preview, Rough, WIP, v1...). Best option: it already has edited pacing.
2. **Raw footage** in `01_Footage/` — pick the main talking-head/screen recording, not
   stock b-roll or the endcard.

Also read `script.md` and `shot-list.md` in the project root if they exist. You need them
for one thing above all: **to know what the video's payoff is, so the teaser can avoid it.**

Transcribe the chosen source fresh. Extract audio first — feeding a multi-hundred-MB video
straight to whisper works but is slow:

```bash
ffmpeg -y -i "$SRC" -vn -ac 1 -ar 16000 <scratch>/audio.wav
mlx_whisper <scratch>/audio.wav --model mlx-community/whisper-small.en-mlx \
  --word-timestamps True --output-format json --output-dir <scratch>
```

Working dir: `<scratchpad>/teaser/<source-file-basename>/`. Never plain `/tmp` (files get
reaped mid-run on this machine).

## Step 1 — Pick the tease

Target 15–40 seconds. Hard stop under 60. Shorter is safer: a teaser that runs long starts
accidentally delivering the video.

Read the transcript hunting for the moment that raises the video's central question, then
**cut before the answer arrives**:

- The cold open / hook, if one was recorded — it was written to open the loop.
- The claim that frames the problem ("most teams are stuck on step one").
- A structural tease: "there are N steps" without listing them, "the last one is the one
  nobody does" without saying what it is.
- A visually interesting beat (graphic, demo glimpse) that makes people ask what they're
  looking at.

Before rendering, write down in one line what the video's payoff is (from the script), and
confirm the chosen span does not contain or heavily imply it. Cutting mid-setup beats
cutting just after the reveal — when in doubt, end earlier.

Boundaries snap to word timestamps: first word onset − 0.15s, last word + 0.3s. Ending
mid-thought is acceptable for a teaser ONLY if it's clearly a deliberate cliffhanger on a
completed clause, never a mid-word chop.

Print the plan before rendering (render-first contract — revisions are cheap):

```
TEASER  0:12–0:41  (29s, from preview export, 16:9 as-is)
  Opens: "This one method is why your app falls over at 10k rows."
  Ends before: the fix (the video's payoff)
  Why it teases: names the pain, withholds the solution
```

## Step 2 — Frame and captions

Same machinery as video-x-clips, same rules:

- **16:9 untouched is the default** (screen-share, mixed, produced inserts). Pure
  talking-head for the whole span → 1:1 center crop (`crop=1080:1080:x:0`, x read off a
  real frame). Scene-detect first (`select='gt(scene,0.25)',showinfo`), look at one frame
  per shot — never classify from spot frames.
- Word-pop captions, mandatory (~80% of X views are muted):

```bash
python3 /Users/vega/.claude/skills/video-shorts/scripts/extract_words.py \
  --json <scratch>/audio.json --start <A> --end <B> --out <scratch>/teaser_words.json

node /Users/vega/.claude/skills/video-motion-graphics/scripts/render.mjs \
  --template /Users/vega/.claude/skills/video-x-clips/assets/captions-wide.html \
  --params "{\"style\":\"danvega\",\"words\":$(cat <scratch>/teaser_words.json)}" \
  --duration <len> --fps <integer source fps> --width 1920 --height 1080 \
  --out <scratch>/teaser_cap
```

Verify caption placement against real frames; spans with produced inserts that carry their
own baked captions need `bottom:210` from the start.

## Step 3 — Render

```bash
ffmpeg -y -hwaccel videotoolbox -ss $A -to $B -i "$SRC" \
  -framerate <same integer fps passed to --fps above> -i <scratch>/teaser_cap/f_%04d.png \
  -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass[out]" \
  -map "[out]" -map 0:a -af "loudnorm=I=-14:TP=-1.5:LRA=11" \
  -c:v h264_videotoolbox -b:v 10M -pix_fmt yuv420p -c:a aac -b:a 192k teaser.mp4
```

Verify at ≥3 spread points: captions styled and placed right, nothing important covered,
the clip really ends before the payoff, duration ≤ 60s.

## Step 4 — Tweet copy

Write `teaser-post.md` next to the clip: 2–3 options, each a distinct angle. Follow Dan's
global writing rules (no em dashes, short sentences, plain language). Rules specific to
teasers:

- **Timing is always vague.** "Coming soon", "new video soon", "working on this one" — never
  a day, date, or "this week". Edits slip; the tweet must never become wrong.
- **The tweet opens the same loop the clip opens.** Never answer the question in the text.
  Name the pain or the promise, not the solution.
- **Build-in-public voice works here.** "Been working on this one for a while" is a valid
  angle for a teaser in a way it isn't for a polished X clip.
- No links (there is nothing to link yet). No hashtags. First line must stand alone in the
  feed. Keep each option under ~200 characters.

**Example** (for a hypothetical video on a slow JPA query):
```
Option A (the pain):
This Spring Boot endpoint works perfectly in every demo. In production
it falls over at 10k rows. Been working on a video about why. Coming soon.

Option B (the promise):
One line of Spring Data code is quietly loading your whole table into
memory. New video soon on how to spot it.
```

The examples above are deliberately about a different topic than whatever video you are
teasing — treat them as shape, not content.

Close the file with a reminder line: when the video publishes, reply to the teaser tweet
with the YouTube link — the teaser thread becomes free distribution for the real video.

## Step 5 — Deliver

- Clip → `/Users/vega/youtube/<Project>/04_Exports/teaser/<name>_teaser.mp4`,
  `teaser-post.md` in the same folder. `open` the folder.
- **Files only, on purpose.** Do NOT upload to the ContentOS shorts board, do NOT call
  `save_social_post`, do NOT schedule anything. Dan posts teasers by hand.
- Report: source used, timestamps, duration, the payoff that was withheld, the tweet
  options, and any candidate moments skipped with reasons.
- Keep the scratchpad — boundary nudges and style swaps are fast re-renders.

## Pitfalls log

Append a dated line every time a run burns you.

- (seed) All video-x-clips/video-shorts ffmpeg pitfalls apply: no drawtext/libass in this
  build (HTML captions only), `-ss` before `-i`, single-image writes need `-update 1`, zsh
  doesn't word-split unquoted vars (write bash script files for loops), odd crop widths
  break x264.
- (seed) render.mjs parses `--fps` as an INTEGER. For 29.97 sources render captions at
  `--fps 29` and feed the PNG sequence to ffmpeg at `-framerate 29`; overlay syncs by
  timestamp, so mixed rates are fine.
- (seed) Plain `/tmp` working dirs get reaped mid-run. Session scratchpad for everything.
- (seed) Raw recordings contain retakes. If cutting from `01_Footage` raw files, watch for
  repeated lines around the chosen span and take the LAST take (Dan re-records until happy).

## What this skill does NOT do

- Promote a published video (video-x-clips) or cut 9:16 Shorts (video-shorts).
- Post or schedule anything, anywhere. It produces files and copy.
- Long-form editing (video-rough-cut), thumbnails/titles (video-packaging), motion
  graphics (video-motion-graphics).
