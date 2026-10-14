---
name: video-broll-research
description: >-
  Researched B-roll: when Dan cites an article, blog post, docs, release notes, a survey, or a
  tweet in a video, find the real source, capture it, and animate it full screen with a
  book-highlighter sweep over the exact passage he is talking about, timed to his words. Dan
  approves every source on a review page before anything renders. Use when Dan says "show the
  tweet", "put the article on screen", "highlight what I'm quoting", "find the source I
  mentioned", or when the video-edit orchestrator reaches the research stage. Needs an approved
  rough cut. Not for diagrams or explainers, or for screenshots of Dan's own demo.
---

# Researched B-roll

```bash
V=/Users/vega/dev/projects/video-editor/tools/vedit/bin/vedit
```

A source card covers the frame: the captured page in a clean browser frame (or the tweet card
itself) on the channel's branded backdrop, a slow push toward the passage, and a yellow
highlighter stroke that sweeps the quoted lines as Dan says them. It lands on V5 in the XML and
in the preview. A whoosh plays as it enters and a tick when the highlight starts.

## 1. Find the moments

```bash
$V research --work WORK
```

Read `WORK/cues/research-options.md`. It lists every sentence that might cite something ("Josh
Long tweeted", "according to the release notes", "Broadcom says..."). It casts a wide net, so
drop the ones that are not citations ("it says step one" in a demo). Also drop a moment that
already shows the source on screen (an animation or a screen recording of the page).

## 2. Find each source (never invent one)

For each real citation, find the actual source:

- If Dan named it or pasted a link (or the project has a `sources.md`), use that.
- Otherwise search the web with his sentence, the words around it, and the video's topic.
  Prefer the primary source: the original post, release notes, the docs page, the tweet itself.
- Open the page and copy the **exact passage** Dan is referring to, character for character.
  The highlight is placed by finding that text on the page.
- If you are not confident it is the thing he meant, ask Dan. Never use a source you cannot
  open, and never paraphrase the quote.

Write `WORK/cues/research-decisions.json`:

```json
{"sources": {"b3": {"url": "https://...", "quote": "exact text from the page",
                    "highlight": "over 60%"}},
 "drop": ["b1", "b2"]}
```

`highlight` is optional: the words Dan says when the sweep should start. Without it, the sweep
starts a third of the way into his sentence. Tweets: use the x.com or twitter.com status URL.
They are captured from X's official embed page, with no login.

## 3. Capture, then Dan approves

```bash
$V research --work WORK --capture
```

Each capture goes to `WORK/research/<id>.png` and `.json`, at 2x. Consent banners get the most
private choice, and leftover overlays are removed. A problem listed as "the quote is not on the
page" means the quote differs from the page text: the output shows the page text nearby, so fix
the quote and capture again.

Show Dan `WORK/review/research.html`: what he said, the URL, the capture, and the highlighted
passage for each source. Nothing renders until he approves. `WORK/research/sources.md` lists
every source with its capture date, for the video description.

## 4. Build

```bash
$V research --work WORK --build
$V sfx --work WORK
```

It refuses a card that would cover a graphic (a list, a popup, a lower third). Drop one or the
other. Then preview and export as usual: cards come along with the graphics.

## Check

Make a contact sheet at each card's start, its highlight, and its end. Check that the highlight
lands on the quoted words, the page is readable at 720p, and the card leaves before Dan's next
point.

## Gotchas

- (2026-10-07) A site banner that is part of the page (not a popup), like Wikipedia's notices,
  stays in the capture. Show it on the review page, and pick a different page if it distracts.
- (2026-10-07) A tweet capture has blank margin around the card. It is trimmed to the card's
  border before the render.
