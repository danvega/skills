---
name: video-ideation
description: Research-driven YouTube video ideation for Dan Vega's channel (Java, Spring, AI, and developer tools). Use this whenever Dan asks for video ideas, wonders what video to make next, wants to know what's trending in the Java/Spring/AI space, asks what topics are doing well on YouTube, or mentions ideation, content planning, or "what should I cover". Even a vague "I'm stuck on what to make" should trigger this skill. Produces a ranked idea brief where every idea is backed by evidence of real demand.
---

# Video Ideation

Generate video ideas for Dan's YouTube channel that are backed by evidence, not guesses. The channel's goal: help developers learn and understand software topics — mainly Java, Spring, and AI — while growing views and subscribers. Growth comes from topics people are *already searching for or talking about*, so every idea in the final brief must cite the signal that suggests demand.

## What good output looks like

A ranked brief of 5–10 ideas saved as a markdown file. Each idea includes: 2–3 title options, the evidence for why it will perform ("why now"), a hook angle for the first 30 seconds, a target search keyword, and a score. Use the template in `assets/idea-brief-template.md`.

## Workflow

### Step 0 — Scope (don't over-ask)

If Dan gave constraints (e.g., "ideas about Spring AI", "something quick to produce"), respect them. Otherwise run the full sweep without asking questions first — the research itself surfaces better questions than guessing upfront.

### Step 1 — Fan out research (run sources in parallel)

Gather signals from four sources. If subagents are available, launch them in parallel — one per source — and have each return a list of candidate topics with evidence. Detailed queries, competitor channels, and outlier math are in `references/research-playbook.md`; read it before starting research.

1. **Dan's own channel data** — his personal MCP tools (names ending in `youtube-get-channel-stats`, `youtube-get-top-videos`, `youtube-search-videos-by-topic`, `blog-search-posts-by-keyword`, `newsletter-search-posts-by-keyword`). Find what already over-performs for him, and which proven topics have follow-up or refresh potential. If these tools aren't connected, note it and continue with the other sources.
2. **YouTube outliers** — videos in the Java/Spring/AI-dev niche that massively outperform their channel's typical numbers. An outlier on a small channel is the strongest signal that the *topic* (not the creator) drives the views.
3. **Community and web trends** — Hacker News, Reddit (r/java, r/SpringBoot, r/programming, r/ClaudeAI), recent framework/tool releases, conference talk lineups. What are developers confused about, excited by, or arguing over *right now*?
4. **Search demand** — what learners type into search: "spring boot X tutorial", "how to Y in java", autocomplete-style variations, Google Trends direction for candidate terms.

### Step 2 — Build a candidate list

Merge findings into 15–20 candidates. For each, keep: topic, source of signal, and the raw evidence (a specific video + view count, a HN thread + point count, a release date). Discard anything with no concrete evidence attached — "this seems interesting" is not a signal.

### Step 3 — Score and rank

Score each candidate 1–5 on the five criteria below; total is out of 25. The weights are implicit in what the criteria measure — demand and timeliness matter most for growth.

| Criterion | What it measures |
|---|---|
| **Demand** | Concrete evidence people want this: outlier views, search volume, hot threads |
| **Timeliness** | Is there a "why now"? New release, announcement, rising trend. Evergreen ≠ 0, but news ≥ evergreen for velocity |
| **Fit** | Matches Dan's strengths and audience (Java/Spring/AI devs). His outperformers skew toward "X in minutes" builds, Spring + AI crossovers, and practical dev-tool walkthroughs |
| **Searchability** | Will it keep collecting views from search for months? Clear target keyword exists |
| **Differentiation** | Can Dan add something the existing videos lack — a Java/Spring angle on an AI topic, a newer version, a working build instead of slides |

Drop anything scoring under 15. Keep the top 5–10.

### Step 4 — Write the brief

Fill in `assets/idea-brief-template.md` for the ranked ideas. Titles should be written like real YouTube titles — specific, benefit-forward, under ~65 characters. Pattern examples from what already works in this niche: "Build a ___ in Minutes", "___ Explained: ___", "I Tried ___. Here's What Happened", "Stop ___ (Do This Instead)".

Save to the working folder as `ideas/YYYY-MM-DD-<topic-slug>-ideas.md` (e.g., `ideas/2026-07-08-spring-ai-ideas.md`, or `-general-` for a full sweep) — the slug prevents collisions when multiple briefs land on the same day. Present the file, leading the summary with the #1 idea and its one-line evidence.

## Principles

- **Evidence over vibes.** Every idea must trace back to something observable. If pressed for why an idea is on the list, the answer should be a link and a number, not a hunch.
- **Topic > creator.** When a video outperforms on a *small* channel, the topic carried it. When a big channel outperforms, it may just be their audience. Weight accordingly.
- **Ride waves Dan can own.** A trending AI topic gets a big multiplier when there's a natural Java/Spring angle — that's the intersection where Dan wins and competition is thin.
- **Don't fabricate metrics.** If a view count or trend couldn't be verified, say "unverified" in the evidence rather than inventing a number.
