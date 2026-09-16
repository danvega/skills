# Historical rough-cut incidents

Evidence retained from earlier runs. These are historical notes, not executable instructions.
The current SKILL.md and editing-rules.md resolve superseded advice.

## Pitfalls log

Append a dated line here every time a run burns you — this log is where the skill earns its keep.

- (seed) `select`/`aselect` desyncs audio on cuts — always trim+concat.
- (seed) `tiny.en` drops words and collapses retakes — `small.en` minimum.
- (seed) A whisper "word" spanning 2s+ hides a pause or a retake inside it — re-window before
  cutting near it.
- 2026-07-16: `whisper` CLI isn't installed on this machine — use `mlx_whisper` (miniforge, on
  PATH) with `--model mlx-community/whisper-small.en-mlx --word-timestamps True`; same JSON output.
- 2026-07-16: the screen-share activity check silently reports 0 scene changes if you pass
  `-v error` — `metadata=print` writes at info level, so `-v error` swallows it and every window
  looks static. Omit `-v error` (or use `-v info`) on the scene-change count; keep `-v error`
  elsewhere. Sanity-check the mechanism against a known-active window before trusting a 0.
- 2026-07-16: Dan edits in a **3840x2160** Premiere sequence, so the 1080p-proxy render drops in
  upscaled 200%. Detect against the proxy (fast), but render the **final deliverable from the
  original source at native resolution** — reuse the same `filter.txt` (cut timestamps are
  resolution-independent), point `-i` at the source, drop the `scale`, and encode 4K with
  `-c:v h264_videotoolbox -b:v 50M -maxrate 60M -bufsize 80M` (libx264 at 4K is far slower).
- 2026-07-23: the noise-floor+6dB threshold badly under-detects on Dan's setup — the RMS
  distribution is bimodal (speech ≈ −20dB median, true pauses −50..−69dB) and 10th-pctile+6
  lands below breath/keyboard noise, so 6-min segments showed 1 "silence". Sanity-check counts;
  when bimodal, detect at ≈15dB below the speech median (−35dB worked) instead.
- 2026-07-23: whisper hallucinated a final sentence *inside* a region silencedetect reported as
  pure silence (end-of-file repeat of an earlier line). Retake keep-last logic then wanted a 55s
  cut to "keep" the phantom take. Before resolving retakes, cross-check each take's words against
  the silence list — a "take" inside detected silence doesn't exist.
- 2026-07-24: two shell traps in the activity-check loop: (1) zsh does not word-split `$range`,
  so `set -- $range` passes "47.79 3.56" as one arg and every window silently reports 0 — the
  sanity-check-a-known-active-window rule caught it; (2) ffmpeg eats stdin inside a
  `printf | while read` loop and mangles the next line's timestamps — always pass `-nostdin`
  to ffmpeg inside read loops.
- 2026-07-23: two retake false-positive shapes on screen-share footage: (1) recurring demo
  phrases ("let's go ahead and rerun this") matched 55s apart — real retakes restart within
  seconds, so distrust matches with a working demo between them; (2) narrate-while-typing — Dan
  says a line, then repeats it while typing it. If the gap between "takes" has scene changes
  (typing), it's narration, not a retake — keep both.
- 2026-07-28: **the screen-share activity check must use a RATE, not a count.** `gt(scene,0.003)`
  fires on a blinking cursor, so "any scene change = keep" protected every long silence: a 22.0s
  gap with 4 hits and an 18.6s gap with 1 hit both survived, and the whole 27-min cut came out at
  2% removed. Real typing/scrolling/build output runs 1–4 changes/sec; idle screens run under
  0.3/s. Threshold at **≥0.5 changes/sec = active (keep)**, below = dead air. Took the same footage
  from 2% to 9% removed. Log the rate for every trimmed window so restoring is one sentence.
- 2026-07-28: the cough/burst detector must be bounded to **short gaps (0.5–2.5s)** and a total
  above-floor duration under ~0.5s. Unbounded, it classified a 10.7s gap as a "cough" and cut 10.4s
  of screen work in one go, and flagged 26 bursts in a single clip. Worse, on screen-share a short
  percussive burst is usually a **keystroke or mouse click**, not a cough — run the scene check on
  the gap first and keep it if the frame is moving. Cut only the burst span (±0.08s), not the whole
  gap, so the natural pause survives.
- 2026-07-28: **`small.en` transcribes zero filler tokens.** 2,431 words across four clips, not one
  `um`/`uh`/`er`. The model normalizes disfluencies away, so the filler-removal step in Step 3 is
  structurally inert with this model and reports a truthful-looking "Fillers cut: 0". An
  `--initial-prompt "Um, uh, so, er, hmm…"` verbatim nudge does NOT recover them (527 vs 528 words,
  still zero). Never report 0 fillers as clean delivery. Fixing this needs a disfluency-preserving
  ASR (large-v3 or similar); until then say the pass did not run.
- 2026-07-28 (Upgrading in the Age of AI): the burst detector flagged 112 "coughs" at or ABOVE
  speech level — whisper's ±300ms word timing bleeds real speech into inter-word "gaps", so a
  loud burst hugging a gap edge is usually the word itself. Require **≥0.15s of quiet at BOTH
  gap edges** (burst isolated mid-gap) and gap ≥0.8s; that took 112 candidates down to 2 real
  coughs. Never cut a burst that touches a gap edge.
- 2026-07-28: whisper drifts the first word of a sentence backwards into a long silence ("All"
  of "All right" timed 1s before sound resumes) and hallucinates stranded words ("OK.") inside
  silencedetect-verified silence. When trimming long silences, trust silencedetect boundaries
  over whisper word times — a cut ending 0.35s before silence_end is safe even when whisper
  claims a word inside the cut. Verify each interior "word" against the silence list before
  shrinking a cut around it.
- 2026-07-23: Dan's feedback on the Tool Calling Advisor cut: coughs/sneezes survived because the
  "audible content above floor+10dB = keep" guard protected them, and silencedetect never flags
  them (the burst itself is loud). Result: motion graphics later landed over coughs. Fix: scan
  word-free gaps ≥0.5s for percussive bursts and cut them as dead air — see the coughs/sneezes
  rule in Step 3. Only voiced, rhythmic laughs riding a beat are protected now.
- 2026-09-14 (ColdFusion intro): at the HEAD of a clip, silencedetect at speech-median−15dB
  missed a soft first word ("The" of "The year is 2026"); whisper had drifted it 3.5s early into
  the silence, so neither source placed it. Leaving ~0.9s of lead before silence_end kept it
  intact (seam transcription confirmed). Head cuts: end no later than silence_end − 0.8s. Also:
  merge overlapping cuts before building keeps; a trimmed silence straddling a retake cut's end
  quietly re-extended the cut by 0.1s (harmless here, not always).
