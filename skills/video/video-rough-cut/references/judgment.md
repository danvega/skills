# Rough-cut judgment

Rules for the `review` decisions. The numbers live in `style/style.json`. These are the calls a
script cannot make. Carried over from the video-rough-cut skill's tested rules (2026-07 to 10).

## Speech always wins

If Dan is talking, keep it, unless it is a retake, a slate, a false start, or a filler. If he
narrates while typing or reads code aloud as it goes in, keep that too.

## Retakes

A retake candidate means sentences start alike within 60 seconds of each other. That is a signal,
not proof.

- A real retake: keep the last complete take. The candidate already cuts from the first take to
  just before the last one, including false starts in between. Approve it.
- If the last take is interrupted or worse, keep an earlier complete take instead. Write a manual
  cut for the bad last take and mark the candidate `keep`, then report it.
- Rhetorical repetition ("It's fast. It's really fast.") and two real demo steps that sound alike
  are not retakes. Mark `keep`.
- Never treat sentences in different source clips as retakes. Intros restate the body's promise.

## Slates and false starts

- A slate ("cut that", "let me try that again") proposes cutting itself and the take before it.
  Check that the take before it is really the bad one. Adjust with a manual cut if the bad take
  started earlier.
- A false start trails off and restarts. Cut it when the restart repeats it. Keep it when it is a
  deliberate aside or a list item.

## Fillers

Standalone um/uh/er/hmm are cut automatically. Hedges ("so", "you know", "basically") stay unless
Dan asks. If a filler carries meaning ("um, no"), keep it.

## Long silent stretches in screen recordings

The script marks every pause over 2 seconds in a screen recording for review, with a screen
activity rate (changes per second). Activity says something moves. It does not say whether the
viewer needs to see it. Make a contact sheet of the start, middle, and end and compare:

- **Code entry** (typing, pasting, fixing imports, new files, switching apps to copy something):
  cut, leaving 0.7 s. The viewer sees the code already in place when Dan speaks again. Never
  speed it up.
- **A result** (a build or test finishing, an app or model response, a page loading): keep the
  moment it lands plus a beat to read. If the wait before it is long, cut the wait and keep the
  end: `{"action": "cut", "leave": 2.0, "keep": "end"}` keeps the last 2 s before Dan speaks.
  Pick `leave` from the contact sheet: when the result appears, plus about 1.5 s to read it.
- **Both in one stretch** (typing, then a run): cut with `"keep": "end"` so only the run and its
  result remain.
- A low activity rate does not mean idle. Typing in a small pane on 4K footage can read near zero.

## Pauses after a question or emphasis

A deliberate beat after a question or a strong point needs at least 0.5 s. If an automatic pause
cut would shorten one, override it with `{"action": "cut", "leave": 0.6}`.
