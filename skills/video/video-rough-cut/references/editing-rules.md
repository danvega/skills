# Editing decisions

## Pauses and speech boundaries

| Silence | Talking-head | Screen-share |
|---|---|---|
| Under 0.6 s | Keep | Keep |
| 0.6 to 2 s | Usually leave 0.4 s | Keep |
| Over 2 s | Usually leave 0.5 s | Leave 0.7 s if idle or wordless code entry; keep a result the viewer must watch |

These are initial settings, pending calibration against a raw/published pair. Deliberate beats
following a question or emphasis need at least 0.5 s; transcript punctuation only catches some.
Screen activity at 0.5 or more scene changes/second means something is happening on screen. It
does not mean the viewer needs to see it: see “Wordless code entry” below. Blinking cursors can
produce isolated changes: use the rate, not “any change.” Verify a known-active window first.
Do not change sample rate or scene threshold without recalibrating the rate threshold. Static
frames do not establish that a running build or long read is useless: inspect context.

The old noise-floor + 6 dB rule under-detected on Dan's bimodal audio. The script starts with the
larger of noise-floor + 6 and an upper-percentile RMS estimate minus 15 dB. Check the actual
silences and adapt when the counts or source audio disagree. Never let an ASR token in verified
silence force retention of a phantom phrase.

For cuts derived from speech timestamps, start from 0.15 s of padding on each side, then listen.
ASR uncertainty can exceed that margin. At clip heads leave at least 0.8 s before detected speech
resumes: a quiet first word has been missed by both ASR and silence detection. The script's
silence candidates retain this extra head margin. Merge cuts before deriving keep intervals.

A word longer than 2 s may contain a pause or retake. If an edit touches it, inspect a roughly
±3 s audio window and re-transcribe only if needed. Cache that window and its source timestamps.

## Wordless code entry

Dan does not want viewers to watch him type, paste, or copy code while nobody is talking. On
screen-share, a span over 2 s with no speech, where the only thing happening is code going into
an editor, gets cut. It does not matter how active the screen is. Leave about 0.7 s, the same as
an idle gap. The viewer sees the code already in place when Dan starts talking again. This covers
typing, pasting, fixing imports, creating or renaming files, and switching apps to copy something.

What stays is wordless footage the viewer needs to watch: a build or test run finishing, an app
or model response arriving, a page showing the result. Trim a long wait in front of it. Keep the
moment the result lands, plus a beat to read it.

Scene changes cannot tell these two apart, so the script does not decide. Every wordless active
window arrives in `classify` with an already padded range. For each one, pull a frame at the
start and at the end and compare them:

- New text in an editor pane, a new file in the tree, or another app in front is code entry.
  Move the entry to `cuts`.
- New output in a terminal, run panel, browser, or chat is a result. Delete the entry and name
  it in the report. If the wait before it is long, cut the wait and keep the landing.
- A window that holds both gets split: cut the code entry, keep the result.

`build` refuses to run while any `classify` entry is left. A low activity rate protects nothing
either. Typing in a small pane on 4K footage can read near zero, and those spans already arrive
as silence cuts. For a long silence cut, glance at its last frame so a one-line result is not
lost with it.

Speech always wins. If Dan narrates while typing, or reads the code aloud as it goes in, keep
it. Wordless code entry is cut, never sped up. `speeds` is for a process the viewer should see
progress on, such as a long build.

## Retakes

Use similar sentence openers and phrase overlap inside roughly 60 seconds as candidate signals,
not proof. Keep the last complete take of a genuine retake group; remove the earlier take and
the intervening gap. If the final take is interrupted, keep the prior complete take and report it.
Never compare across source clip boundaries: intros often restate the body's promise.

Check that each take is audible. A transcript can hallucinate an earlier sentence in silence.
Screen work between similar phrases often means two real demo actions, not a retake. Narration
repeated while typing also survives. Slates (“again,” “take two”) support a retake decision.
Record the group, all source times, and the chosen take so revisions are straightforward.

## Fillers and wordless noises

`small.en` has omitted every filler token on real runs, even with a verbatim initial prompt.
A report of zero detected fillers does not mean clean delivery. Default to “fillers not
analyzed.” A larger ASR model is an experiment, not a proven fix. Benchmark alternatives on
known audible fillers before changing the default.

Cut a confirmed standalone um/uh/er/hmm only after listening with surrounding words; retain
hedges (“so,” “you know,” “basically”) unless explicitly requested. Do not let automatic token
matching cut words that happen to look like fillers.

For coughs/sneezes, inspect short word-free gaps of roughly 0.8 to 2.5 s. A candidate burst must
be isolated by at least 0.15 s of quiet on both sides, and total above-floor burst duration
should be under roughly 0.5 s. Speech timing often bleeds into gap edges: never classify such
edge energy as a cough. In screen-share, check activity first; keystrokes and clicks are common.

Remove only the confirmed burst with about 0.08 s padding, keeping the natural pause. Do not
cut an entire long gap because it contains a transient. Uncertain classification alone is not
a safe cut; listen. A confirmed wordless percussive interruption can go, per Dan's preference.
Keep voiced, rhythmic laughs and reactions that belong to the delivery.
