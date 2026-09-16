---
name: spring-office-hours-prep
description: >-
  Run both local publishing steps for a Spring Office Hours episode back to back: rough-edit the
  raw recording into the publish-ready mp3 and transcript, then assemble the Transistor title,
  description and Show Notes. Ends at the Transistor handoff with the clipboard loaded. Use
  whenever Dan wants an episode prepped in one go: "prep S5E21", "get S5E21 ready", "edit and
  write up this episode", "run the prep chain", or hands over a recording and wants everything
  short of publishing. Do NOT use for the spring.io PR (spring-office-hours-spring-io-pr, which
  requires the episode to already be live on Transistor), and do NOT use when Dan asks for only
  the audio (spring-office-hours-edit) or only the notes (spring-office-hours-show-notes).
---

# Spring Office Hours: Prep

Two skills, one command. This runs `spring-office-hours-edit` then
`spring-office-hours-show-notes` for one episode, resolving their shared inputs once instead of
twice, and stops at the point where Dan has to take over.

This skill adds no editorial judgment of its own. It sequences, it does not decide. Every rule
about boundaries, link selection and verbatim descriptions lives in the two child skills and
still applies in full.

## The pipeline this sits in

1. **prep** (this skill): edit + show notes. Local, no accounts, fully automatable.
2. **Transistor** (Dan): upload the mp3, paste title and description, publish. Manual.
3. **spring.io PR** (`spring-office-hours-spring-io-pr`): needs the embed hash from the public
   RSS feed, which does not exist until step 2 is done.

Step 2 is a hard gate, not a convenience gate. That is why this is `prep` and not `publish`.

## Step 0: resolve the shared inputs once

Both child skills need the same three things, and both would otherwise go find them separately.
Resolve them here and pass them down as skill arguments.

- **Episode token** (`S5E21`). Ask if Dan did not say.
- **Raw recording.** Look in `/Users/vega/youtube/spring-office-hours/raw/` first, then
  `/Users/vega/youtube/spring-office-hours/S5/`, matching the token in the filename. Audio-only
  beats the 2GB mp4 but either works. If neither has it, ask before downloading anything; Dan
  usually already has the file.
- **YouTube video id.** One search, reused by both:

  ```bash
  yt-dlp --no-warnings --flat-playlist --print "%(id)s | %(channel)s | %(duration)s | %(title)s" \
    "ytsearch8:Spring Office Hours $EP"
  ```

  Pick the SpringDeveloper hit whose duration matches the episode, not just the channel. A Short
  with the same title has bitten this before. Confirm the duration against the raw file with
  `ffprobe` while you are here; a large mismatch means you have the wrong video or a partial
  recording, and both child skills would inherit that error.

## Step 1: edit

Invoke `spring-office-hours-edit` with the token, the resolved raw path, and the video id.

Do not summarise or shortcut its report. The boundary quotes it prints are the only cheap way
Dan can catch a bad cut without listening to the whole episode, so surface them verbatim.

Stop the chain if the edit reports something Dan needs to rule on before notes are worth
writing: a boundary that did not match its formula and reads wrong, a suspected whisper
repetition loop in the sign-off region, or a runtime far off the raw duration.

## Step 2: show notes

Invoke `spring-office-hours-show-notes` with the token, the transcript path the edit just
produced, and the same video id.

## Step 3: hand off

One consolidated report. Dan is about to go do manual work, so give him exactly what that needs:

- The boundary quotes and runtime from the edit.
- The title and description, and any place the planned description does not match what actually
  happened on the live show.
- The Show Notes links, plus anything mentioned that could not be resolved to a live URL.
- Confirmation that the mp3, `.srt` and `.txt` are in
  `/Users/vega/youtube/spring-office-hours/exports/` and the clipboard holds the rich-text
  description.

Then state the gate plainly: upload and publish on Transistor, and once it appears in the feed,
`spring-office-hours-spring-io-pr` finishes the job. Do not start that skill yourself, and do not
poll the feed unless Dan asks. The feed lags publication by several minutes, so an immediate
check would fail and read as an error when nothing is wrong.

## Pitfalls log

Append a dated line every time a run burns you.

- (seed 2026-08-17) The two child skills each resolve the YouTube video independently and each
  carry the same "pick by duration, a Short can share the title" pitfall. Resolving once in
  step 0 removes one chance to get it wrong. Do not let it drift back to two lookups.
- (seed 2026-08-17) Do not collapse this into the PR step. The RSS embed hash does not exist
  until Transistor has published, and a PR built with a placeholder hash ships a broken player.

## What this skill does NOT do

- Any editorial work of its own. It sequences two skills that already know their jobs.
- Transistor. No uploading, no publishing, no API calls.
- The spring.io PR.
- danvega.dev, YouTube metadata, thumbnails, or social posts.
