---
name: video-packaging
description: Turn one chosen video idea into a congruent package — final title, thumbnail concept, and first-30-seconds intro — locked into the video's ContentOS project, for Dan Vega's YouTube channel. Use when Dan has decided what to film and wants it packaged, or mentions titles, thumbnails, hooks, intros, or "packaging" for a specific video. Input can be an idea from a video-ideation brief, a plain topic, or source material Dan hands over — code, a repo, a blog post, an article, release notes, or documentation the video will be based on. Figuring out WHAT to make is `video-ideation`; this skill packages an idea that is already chosen.
---

# Video Packaging

The idea sets a video's ceiling; the packaging decides whether it gets there. A viewer decides in a fixed sequence: the **thumbnail** earns the look, the **title** earns the click, the **intro** earns the watch. Those three are the package, and they live or die together.

## The one rule: congruence

The thumbnail makes a promise, the title confirms it, and the first 30 seconds start keeping it. Three strong pieces that tell three different stories lose to three decent pieces that tell one story — a mismatch reads as a bait-and-switch, and the viewer clicks away feeling lied to. So never optimize a piece in isolation: a clever title that drifts from the thumbnail's promise gets cut, no matter how good it is on its own.

## Workflow

### Step 1 — Understand what the video is actually about

Dan often hands over source material with the idea: code or a whole project, a blog post, an article, release notes, or documentation the video is built on. Read it before writing anything — it is the ground truth for what the video contains, and it's where the specifics that make packaging land come from: the exact feature names, version numbers, before/after deltas, a surprising result, the gotcha that cost an afternoon. Mine it for concrete, quotable details; a title or intro built from them beats one built from the topic label alone. If the material is large (a repo, long docs), skim for what's demonstrable on camera — the parts of it the video will actually show.

If the video has a ContentOS project (`mcp__contentos__list_projects`, match by topic), pull its context before writing anything:

- `get_brief` — the developed idea's promise, demand evidence, hook angle, and target keyword.
- `get_demo_plan` — the demo's final frame is the leading thumbnail-concept candidate, and the companion repo is the description link (this is `video-demo-design`'s handoff).
- `list_videos` — a GO brief auto-generates candidate hooks and thumbnail ideas on the long-form video. Treat these as raw material to beat, not decisions already made.

Then write the video's promise as one sentence: who it's for and what they walk away with — combining the brief's demand signal (why people want this) with what the source material proves the video can deliver. Every title, thumbnail concept, and intro line must trace back to this sentence.

### Step 2 — Titles (8–10 options)

- Under ~65 characters, benefit-forward, target the keyword early where it fits naturally.
- Write real YouTube titles, not descriptions. Patterns that work in this niche: "Build a ___ in Minutes", "___ Explained: ___", "I Tried ___. Here's What Happened", "Stop ___ (Do This Instead)", "___ Changed How I ___".
- Vary the mechanism across options — curiosity, specificity (numbers, versions, named tools), contrarian take — then mark a top pick and say why, citing the evidence.

### Step 3 — Thumbnail concept (a creative brief, not an image)

Produce 2–3 concepts. Each specifies: the focal subject and expression, on-image text of **4 words or fewer**, composition (rule-of-thirds placement, where the face vs. text goes), color/contrast direction, and what to leave out. Two hard rules:

- Thumbnail text must **not repeat the title** — the pair is read together, so the text complements the title (title: "Spring AI 2.0: Everything New" → thumbnail: "IT ALL CHANGED"), never duplicates it.
- It must be legible at ~120px wide. If a concept needs a paragraph to explain, it won't survive shrinking.

The deliverable is a brief Dan hands to his thumbnail process — describe the image, don't attempt to render it.

### Step 4 — Intro (the first 30 seconds, scripted)

Write 2–3 openings, ~60–90 words each, labeled by style (cold open, result-first, contrarian). Every opening must:

1. **Confirm the click in the first sentence** — restate the promise the thumbnail and title made, in different words.
2. **Give a reason to stay** — an open loop, the stakes, or a credibility marker (a number, a demo on screen, a result).
3. Contain zero throat-clearing: no "hey everyone, welcome back", no channel intro, no agenda reading. The video starts mid-stride.

### Step 5 — Congruence check

Before presenting anything, audit the recommended combination in a table: the core promise, what the thumbnail says, what the title says, what the intro's first sentence delivers. If any leg tells a different story, fix it — don't ship a package that fails its own rule.

### Output

Present the recommended trio (one title + one thumbnail concept + one intro) first, then the alternatives. Once Dan picks — not before; the lock is his call — save the package into ContentOS:

- `update_video_packaging(slug, title, hook, thumbnailConcept)` with the picked trio. Only pass what's locked; the tool leaves other fields alone.
- `set_pipeline_stage TITLE_LOCKED` and `INTRO_WRITTEN`. Leave `THUMBNAIL_READY` to `video-thumbnail` — that stage means rendered art, not a concept.

ContentOS is the source of truth for the locked package; `video-thumbnail` reads the concept from there when it renders the art. If there's no ContentOS project or the MCP tools aren't connected, say so and fall back to saving `packaging/YYYY-MM-DD-<video-slug>.md` in the working folder instead.

Then publish the package as an artifact (via the Artifact tool) so Dan has a shareable brief to reference while filming. Load the `artifact-design` skill first, write the HTML to the scratchpad, and publish with favicon 🎬. The artifact carries the full package — the locked trio plus every alternative — structured for scanning:

- Header: video topic, date, target keyword, effort, source link — then the promise as a callout.
- The recommended package as the lead card: the picked title, thumbnail Concept A, and the recommended intro. Render the thumbnail concept as a rough CSS layout mock at 16:9 (labeled "layout mock, not final art") alongside a 120px-wide copy as the shrink test — it proves legibility instead of asserting it.
- Then the alternatives: remaining titles (each tagged with its mechanism), other thumbnail concepts with their risks, alternate intros, the congruence table, and the key facts/gotchas mined from the source material for building the demo.
- Set intro scripts in a serif reading face so they read as spoken scripts; set titles and code in mono. Support light and dark themes.
- Keep the artifact URL stable across revisions: republish the same HTML file path when iterating on a package in-session, or pass the existing URL when updating from a later conversation.

The ContentOS record holds the locked trio; the artifact is the presentation layer Dan references while filming.

## Principles

- **Congruence over cleverness.** The best individual piece loses if it breaks the shared story.
- **Specific beats hype.** Version numbers, named tools, and concrete results out-click superlatives in a developer niche.
- **Curiosity without bait.** Open a gap the video actually closes; never promise what the content doesn't deliver.
- **The package is a hypothesis.** Note the target keyword and the promise so title/thumbnail can be revisited if the video underperforms its first 48 hours.
