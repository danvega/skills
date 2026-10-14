---
name: video-x-clips
description: >-
  Cut a finished long-form video into 1 to 3 native clips for X (Twitter), 16:9 or 1:1 with
  burned-in captions, each with ready-to-paste post copy written to start conversations. Runs
  on the final export in 04_Exports. Use when Dan wants clips for X, wants to tweet or promote
  a published video on X, or asks for "X clips" or "something to post on Twitter". Dan posts
  them himself. Not for editing the long-form video (video-edit) or vertical shorts.
---

# X clips

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
R=/Users/vega/dev/projects/video-editor/tools/render/render.mjs
S=/Users/vega/dev/danvega/skills/skills/video/video-x-clips
```

Pull the moments from a finished video that will get developers replying, and deliver each as
a finished clip plus post copy. An X clip succeeds when people reply, quote, or tag a
coworker, not when they watch to the end. One strong clip beats three weak ones. Zero is a
fine answer for a tutorial with no takes in it.

## Format

- MP4, H.264 and AAC. 16:9 (1920x1080) or 1:1 (1080x1080).
- 140 seconds or less as encoded, and 512 MB or less. 45 to 90 seconds is the sweet spot.
- Most X views are muted, so captions are burned in.
- Native upload only. The YouTube link goes in a first reply, never in the post.

## 1. Transcript

Use the final export in `~/youtube/<Name>/04_Exports/`. If it is empty, say so and ask.
Clips must match the published video, so never cut from edit intermediates.

```bash
$V publish ~/youtube/<Name>/04_Exports/<Name>.mp4
```

This is the video-transcribe publish step. It reuses an existing transcript of the same file.
Work in `~/youtube/<Name>/edit/x-clips/`. Read `edit/publish/transcript/<id>.phrases.md` to
find moments. The words with times are in `<id>.words.json` next to it.

## 2. Pick the moments

Look for conversation starters, best first:

- A take a reasonable developer could push back on ("I would not start with JPA").
- Myth busting or wrong way and right way.
- A complete mini argument: setup, claim, reasoning, landing. X allows 60 to 90 seconds of
  build-up, but the clip ends on the landing.
- Produced cold opens and story graphics. They stop the scroll better than talking head.

The claim, or the visual that carries it, must land in the first 3 seconds. Start a clip
0.15 s before its first word and end it 0.3 s after its last.

If Dan named a moment ("clip the hot take about JPA"), skip the ranking. Otherwise show the
plan and wait for his OK before rendering:

```
CLIP 1  0:00-0:42  (42s, produced cold open, 16:9)
  Hook: "Can you trust AI-generated code?"
  Why people reply: they have their own trust stories
Skipped: findAll teardown. Good tutorial, but nothing to argue with.
```

## 3. Frame

Look at one frame per shot in the span (`ffmpeg -i SRC -ss A -to B -vf
"select='gt(scene,0.25)',showinfo" -f null -`). Spot frames miss full-screen inserts.

- **Screen share, mixed, or produced inserts:** 16:9 as is. This is most of Dan's videos.
- **Talking head for the whole span:** 1:1 crop centered on his face, read off a real frame.
  If the crop cuts a lower third or callout, use 16:9.

## 4. Captions

```bash
python3 $S/scripts/clip_words.py --words <transcript>/<id>.words.json --start A --end B \
  --out clip1/words.json
echo "{\"style\":\"danvega\",\"bottom\":90,\"words\":$(cat clip1/words.json)}" > clip1/captions.json
node $R --template $S/assets/captions-wide.html --params-file clip1/captions.json \
  --duration LEN --fps FPS --width 1920 --height 1080 --out clip1/frames --mov clip1/captions.mov
```

- `FPS` is the export's exact rate from `ffprobe` (`30000/1001`, not `29.97`).
- For 1:1, render at `--width 1080 --height 1080` with `"bottom":130`.
- Check a frame against the video. If the captions cover code or a baked-in graphic, raise
  `bottom` or move the clip a beat. Produced inserts with their own caption line need
  `"bottom":210`.

## 5. Render

```bash
ffmpeg -y -ss A -to B -i SRC -i clip1/captions.mov \
  -filter_complex "[0:v][1:v]overlay=0:0:eof_action=pass[v]" -map "[v]" -map 0:a \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11" -c:v h264_videotoolbox -b:v 10M -pix_fmt yuv420p \
  -c:a aac -b:a 192k clip1/out.mp4
```

For 1:1, crop first: `[0:v]crop=1080:1080:X:0[c];[c][1:v]overlay=...`.

Check each clip at the hook, the middle, and the payoff. Captions are timed and placed right,
nothing important is covered, the encoded length is 140 s or less, and the file is 512 MB or
less.

## 6. Post copy

Write `x-posts.md` with 2 or 3 options per clip and one first reply.

- Write as Dan, in first person ("I found", never "Dan finds").
- The first line stands alone in the feed. Give the claim or the tension, not a summary of
  the clip's first sentence.
- End with an opening for replies when it fits: a real question ("Would you have caught it in
  review?") or a quotable take. No engagement bait.
- No hashtags and no links. The first reply is "Full video: URL".
- Under 200 characters. Each option takes a different angle: the take, the question, the
  story.

## 7. Deliver

Copy the clips to `~/youtube/<Name>/04_Exports/x/<Name>_x1_<slug>.mp4` with `x-posts.md`
beside them, and `open` the folder. Report each clip's times, length, format and why, and
the candidates you skipped. Keep `edit/x-clips/` so boundary nudges are quick re-renders.

## Gotchas

- The installed FFmpeg has no `drawtext` or `libass`. Captions go through the HTML renderer.
- (2026-07-30) The 140 s cap applies to the encoded file. A 139.8 s plan can land at 140.3 s
  after the keyframe snap and fail the upload. Check the output length.
- X re-encodes every upload. More than 10 Mbps only slows the upload.
