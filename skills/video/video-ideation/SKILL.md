---
name: video-ideation
description: Research-driven YouTube video ideation for Dan Vega's channel (Java, Spring, AI, and developer tools). Use this whenever Dan asks for video ideas, wonders what video to make next, wants to know what's trending in the Java/Spring/AI space, asks what topics are doing well on YouTube, or mentions ideation, content planning, or "what should I cover". Even a vague "I'm stuck on what to make" should trigger this skill. Produces ranked ideas backed by evidence of real demand, saved into the ContentOS idea backlog.
---

# Video Ideation

Generate video ideas for Dan's YouTube channel that are backed by evidence, not guesses. The channel's goal: help developers learn and understand software topics — mainly Java, Spring, and AI — while growing views and subscribers. Growth comes from topics people are *already searching for or talking about*, so every idea saved must cite the signal that suggests demand.

## What good output looks like

5–10 ranked ideas saved into the **ContentOS idea backlog** via `mcp__contentos__save_idea` (they show up in the Ideas inbox at `/ideas` for review and promotion into projects — do not save them into his repo or working folder, and do not publish an artifact). Each idea includes: 2–3 title options, the evidence for why it will perform ("why now"), a hook angle for the first 30 seconds, a target search keyword, and a score. Step 4 maps these onto `save_idea`'s fields.

## Workflow

### Step 0 — Scope (don't over-ask)

If Dan gave constraints (e.g., "ideas about Spring AI", "something quick to produce"), respect them. Otherwise run the full sweep without asking questions first — the research itself surfaces better questions than guessing upfront.

### Step 0.5 — Read the idea backlog (avoid repeating ideas)

Before researching, call `mcp__contentos__list_ideas` (no filter) — the ContentOS idea backlog is the record of every past suggestion. This can run while the Step 1 research agents are working, but must finish before Step 2's merge. Then:

- **Already filmed** (it appears in his recent uploads from the channel-data source): exclude it, and exclude near-duplicates of it.
- **PROMOTED**: it's already in the project pipeline — exclude it and near-duplicates of it.
- **ARCHIVED**: Dan passed on it — exclude it unless the evidence has materially strengthened since (new release, new outlier, new deadline); then it may re-enter, marked "previously archived, re-scored" and citing the *new* evidence.
- **NEW or SHORTLISTED, evidence unchanged**: don't re-save it, but mention it in one line under a "Still in your inbox from last time" note so it isn't silently forgotten.
- **NEW or SHORTLISTED, evidence materially strengthened**: mention it in that same note with the new evidence and suggest bumping it; don't create a duplicate.

Match on topic, not exact title strings. Legacy fallback: idea briefs from before the backlog existed (before July 2026) live as artifacts titled `Video Ideas — <date>`; if the backlog is suspiciously empty, list artifacts and WebFetch the most recent one or two as an extra dedupe source. If the ContentOS MCP tools aren't connected, say so and ask Dan whether to proceed without the backlog — running without it risks duplicate suggestions and the results will only live in the conversation.

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

### Step 4 — Save the ideas into ContentOS

The ContentOS idea backlog is the single destination — do NOT publish an artifact, save files into Dan's repo, or call `create_project` (ideas graduate to projects later, from the Ideas inbox or via `promote_idea`).

Titles should be written like real YouTube titles — specific, benefit-forward, under ~65 characters. Pattern examples from what already works in this niche: "Build a ___ in Minutes", "___ Explained: ___", "I Tried ___. Here's What Happened", "Stop ___ (Do This Instead)".

One `mcp__contentos__save_idea` call per ranked idea:

- `title`: the strongest title option. `hook`: the hook angle. `whyNow`: the evidence — specific link + number + date, e.g. "X's video hit 180K views on a 9K-sub channel 2 weeks ago". `targetKeyword`: the primary search phrase. `score`: the total out of 25.
- `source`: `video-ideation <YYYY-MM-DD>` so it's traceable to this run.
- `notes`: markdown with the rest of the per-idea detail — alternate title options, per-criterion scores (Demand/Timeliness/Fit/Searchability/Differentiation), format (build-along / explained / comparison / first look), estimated effort (S/M/L), and any extra evidence that didn't fit `whyNow`. Each saved idea must stand alone: a future session should reconstruct "what this is and why it was suggested" from the idea record itself.

Also save each **watchlist** topic (rising but didn't make the cut) as an idea: no `score`, `source` = `video-ideation <YYYY-MM-DD> watchlist`, and `notes` stating the signal to watch and when to re-check. Unscored ideas sort to the bottom of the inbox, so they won't crowd the ranked ones.

Don't re-save anything Step 0.5 found already in the backlog.

### Step 5 — Present the results

Summarize the ranked list in the conversation, leading with the #1 idea and its one-line evidence; note any theme that emerged across sources and any data gaps. Point Dan at the Ideas inbox (`http://localhost:8888/ideas`) to review, shortlist, or promote. When Dan picks an idea to film, hand off to the `video-packaging` skill to develop its title, thumbnail concept, and intro as one congruent package.

## Principles

- **Evidence over vibes.** Every idea must trace back to something observable. If pressed for why an idea is on the list, the answer should be a link and a number, not a hunch.
- **Topic > creator.** When a video outperforms on a *small* channel, the topic carried it. When a big channel outperforms, it may just be their audience. Weight accordingly.
- **Ride waves Dan can own.** A trending AI topic gets a big multiplier when there's a natural Java/Spring angle — that's the intersection where Dan wins and competition is thin.
- **Don't fabricate metrics.** If a view count or trend couldn't be verified, say "unverified" in the evidence rather than inventing a number.
