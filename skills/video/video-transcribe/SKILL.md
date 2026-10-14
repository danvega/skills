---
name: video-transcribe
description: >-
  Transcribe raw video or audio recordings into checked word-level transcripts for the edit
  pipeline, using parakeet-mlx locally with a coverage check that recovers any speech the
  model skipped and a glossary pass for terms it gets wrong. Use when Dan wants a recording
  transcribed, when an edit is starting and the sources have no transcript yet, or when the
  video-edit orchestrator runs the transcribe stage. Also makes the transcripts of a finished
  export for publishing (srt, vtt, txt, json, and a clean transcript in 05_Transcripts) when Dan
  says "transcribe the export", "captions for PublishWell", or "a transcript I can share". Not
  for show notes or burned-in captions.
---

# Transcribe

Turn source recordings into `words.json` transcripts that every later stage reads. One
command does the work. Your job is to run it, read the summary, and resolve anything it flags.

## Run

```bash
/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit transcribe /abs/clip1.mp4 /abs/clip2.mp4
```

- `--work DIR` sets the working folder. The default is `<project>/edit` for files under
  `~/youtube/<project>/`, else `edit/` next to the first source. Never put it in the skills repo.
- Pass every source of one video in one call. The model loads once.
- A rerun skips sources whose content and settings are unchanged, so it is safe to repeat.
- `--decoding beam` is slower. Use it only to retry a source with an unresolved gap.

## Read the summary

The command prints JSON per source. Check:

| Field | Meaning | Action |
|---|---|---|
| `vfr: true` | Variable frame rate, usual for screen recordings | Tell Dan. The rough cut converts it before cutting. |
| `gaps` | Loud stretches with no words in the first pass | Nothing. Each was re-transcribed as a slice, greedy then beam. |
| `recovered_words` | Words the slices heard that the full pass missed | Nothing. They are already in the transcript. |
| `review` | Loud stretches of 1.5 s or more still without words | Read the transcript around each one. Laughter, music, or typing is fine. A missing sentence in a solo video is not: report its times. |
| `corrections` | Glossary fixes applied | Spot-check them in `<id>.coverage.json`. |

A solo recording usually shows zero gaps. A two-person conversation shows more, mostly
crosstalk and laughter, and a few short `review` spots are normal there.

## Outputs

In `<work>/transcript/`: `<id>.words.json` (the transcript), `<id>.words.tsv` and
`<id>.phrases.md` (compact views for reading), and `<id>.coverage.json` (the evidence).
`<work>/sources.json` maps each source id to its path, hash, duration, and frame rate.
`<work>/audio/<id>.wav` is kept for later stages.

Read `phrases.md`, not `words.json`. Each line is one sentence with its word range, like
`[37-40] 13.68-16.08 (+0.2s) Now picture 50 applications.`

## Transcripts to share or publish

When Dan wants a transcript of a finished export (captions, PublishWell, one to send someone):

```bash
/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit publish ~/youtube/<Name>/04_Exports/<Name>.mp4
```

It transcribes the export in its own work folder (`edit/publish`, never the edit's sources) and
writes `<Name>.srt`, `.vtt`, `.txt`, `.json`, and `<Name>-clean.md` to the project's
`05_Transcripts`. Standalone "uh" and "um" are dropped. Then read the text and fix what came
out wrong, in two files in `edit/publish/`, and run it again:

- `fixes.txt`: this video's spellings, `wrong => right` (case, punctuation, and spaces ignored;
  an empty right side drops the words). Fix spellings and terms, never Dan's wording. A term
  that will recur goes in `style/glossary.txt` instead.
- `sections.txt`: `0:58 What is TrueSource?`, one per line, for the headings in `-clean.md`.
  Take them from the edit's clip order.

## Glossary

When a term comes out wrong, add a line to
`/Users/vega/dev/projects/video-editor/style/glossary.txt` (`wrong => right`) and rerun. Only
the glossary step runs again. Add only terms that will recur. A one-off mishearing is fixed
in the transcript plan, not the glossary.

## Gotchas

- (2026-10-07) parakeet-mlx default 120 s chunking dropped a 10 s passage, and
  `--chunk-duration 0` alone dropped a phrase. vedit always runs
  `--chunk-duration 0 --local-attention`. Do not call parakeet-mlx directly with other settings.
- (2026-10-07) A dropped phrase can split into short pieces around a pause ("Three," then
  "where will Advisor run?"). The coverage check merges nearby pieces before measuring them.
- (2026-10-07) Slice timestamps drift from the full pass, and slices start mid-word. Recovery
  aligns slice words to the transcript by text and time, and skips words that sit on top of
  existing words. Matching by time alone threw away real words. Matching by text alone
  anchored on common words ("a", "that") seconds away.
- (2026-10-07) In crosstalk, each pass can hear a different speaker. On S5E25, only the beam
  slice caught "My employer does not care." That is why a beam pass runs after greedy.
- (2026-10-07) The first model download can stall and then report a misleading
  "config.json not found". vedit downloads the model as its own step first.
- (2026-10-07) The Hugging Face cache stores the model through symlinks, so plain `du` shows
  about 400 KB. Use `du -shL` to see the real 2.5 GB.
