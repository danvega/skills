---
name: video-develop-idea
description: Research, refine, and scope a single video idea Dan already has — validate demand with evidence, find the angle competitors are missing, and define what the video covers, ending in a go / reframe / park verdict saved as the project's brief in ContentOS. Use whenever Dan brings his own idea rather than asking for new ones — "I want to make a video about X", "is X worth a video?", "help me scope this video", "research this topic for a video", "what should I cover in a video on X", "how should I angle this". Finding ideas from scratch is `video-ideation`; turning a settled, scoped idea into a title/thumbnail/intro is `video-packaging`. This skill is the bridge between them.
---

# Develop Idea

Dan arrives with an idea; the job is to pressure-test and shape it, not to admire it. A good session answers three questions with evidence: **is there demand** for this, **what angle** wins against what already exists, and **what exactly should the video cover**. The honest outcomes are *go*, *reframe* (the idea is close but a different angle or framing is stronger), or *park* (the evidence says wait or skip — saying so saves Dan a week of production on a video nobody asked for).

Present the resulting brief **directly in the conversation** — no artifact, no file saved to a repo or working folder. The durable record is **ContentOS** (Step 6): saving the brief there is what makes the verdict actionable, and on a GO it kicks off the downstream automation.

## Workflow

### Step 1 — Capture the seed

Restate the idea as you understand it in one or two sentences and note any constraints Dan gave (deadline, effort level, a specific release it ties to). Then check what he actually asked for:

- **Full development** ("is this worth making?", "help me with this idea") → run all steps.
- **A partial ask** ("just help me scope it", "what's a good angle?") → do that part well; only pull in other steps if their findings change the answer. Don't run a demand sweep Dan didn't ask for when he's already committed to filming.

Don't interrogate him upfront — the research surfaces better questions than guessing does. Ask at most one clarifying question, and only if the idea is genuinely ambiguous.

### Step 2 — Validate demand

Research pointed at *this one topic*, not a broad sweep. Tactics, tool names, and the channel list are in `references/research-guide.md` — read it before starting. Run sources in parallel (via subagents if available):

1. **Dan's own data** — has he (or his blog/newsletter) covered this or adjacent topics, and how did it perform? Prior over-performance on a neighboring topic is strong evidence; a prior flop is worth knowing too.
2. **YouTube signal** — do existing videos on this topic pull outlier views relative to their channel size? No videos at all is ambiguous: either an open lane or no demand — search volume decides which.
3. **Community signal** — recent HN/Reddit threads, release notes, conference talks touching the topic. Recurring confusion is tutorial demand; heated debate is "explained/opinion" demand.
4. **Search demand** — what learners type, whether the head terms are rising or flat, and whether what currently ranks is stale.

Every claim carries its evidence (a link and a number). If a number can't be verified, say "unverified" — never invent one.

### Step 3 — Map the competition

This is where "refine" happens: **the angle falls out of the gap.** Look at the 3–6 videos that currently own this topic and note for each: what it covers, its format, its framework/tool versions, and what it *skips or gets wrong*. Then ask:

- What does every existing video miss that Dan can deliver — a newer version, a working build instead of slides, the Java/Spring angle on an AI-world topic?
- Is the topic saturated by big channels (hard to win on the same framing) or held by outdated/low-quality results (easy win)?

Propose 2–3 angle options, each stated as a promise ("who it's for and what they walk away with"), and recommend one with the reasoning attached.

### Step 4 — Scope the video

Define the video concretely enough that Dan could start outlining:

- **In**: the 3–5 things the video covers, in rough order.
- **Deliberately out**: adjacent material that would bloat it — name it so it's a decision, not an accident. If something cut is strong on its own, flag it as a possible follow-up video.
- **Demo plan**: what's actually shown on camera — the build, the before/after, the result that proves the promise. Dan's outperformers are "show, don't slide" videos; a scope with nothing demonstrable is a warning sign.
- **Assumed knowledge**: what the viewer already knows, so the video starts at the right altitude.
- **Rough shape**: estimated runtime and effort (quick win vs. multi-day build).

Scope serves the chosen angle: everything "in" must support the one promise from Step 3. When a list grows past one promise, that's two videos.

### Step 5 — Verdict and brief

Present the brief in the conversation, verdict first:

- **Go** — demand confirmed, angle chosen, scope defined. Lead with the one-line reason backed by the strongest evidence.
- **Reframe** — the topic has legs but a different angle is stronger. Show the original vs. the reframe and why the evidence favors it.
- **Park** — weak or falling demand, or a saturated field with no gap. Say so plainly, cite the evidence, and note what would change the verdict (an upcoming release, a rising trend to watch).

Then the supporting sections: the demand evidence, the competitive map with the gap, the angle options with the pick, and the scope. Close a *go* with the handoff: `video-packaging` reads the saved brief via `get_brief`, and `video-project` scaffolds the project folder when he's ready to film.

### Step 6 — Record it in ContentOS

The brief must outlive the conversation. Route by where the idea currently lives (`mcp__contentos__list_projects`, `mcp__contentos__list_ideas`):

- **A project already exists** → `save_brief(slug, verdict, markdown)`. One brief per project; saving again replaces it, which is exactly right for a re-scoped idea.
- **It's a backlog idea, verdict GO or REFRAME** → `promote_idea` to create the project, then `save_brief` on the new slug.
- **It's a backlog idea, verdict PARK** → `update_idea_status` to ARCHIVED with notes citing the evidence and what would change the verdict. Don't create a project for a parked idea.
- **No record anywhere** → GO/REFRAME: `create_project`, then `save_brief`. PARK: `save_idea` into the backlog with the park reasoning in notes — the research shouldn't evaporate just because the answer was no.

The markdown body is the full brief: demand evidence, competitive map, chosen angle, scope in/out, demo plan, hook. On a **GO**, also `set_pipeline_stage IDEA_DEVELOPED` and, if the research sharpened it, `update_project` with the better one-sentence idea. Know what the save triggers so you don't duplicate it: a GO brief auto-creates the long-form PLANNING video and generates packaging candidates (hook/thumbnail ideas) — don't hand-create the video or pre-write packaging here.

If the ContentOS MCP tools aren't connected, say so explicitly and flag that the brief exists only in the conversation until it's saved.

## Principles

- **Evidence over vibes.** Same rule as ideation: every claim traces to a link and a number, or is labeled unverified.
- **Park is a win.** A well-evidenced "don't make this" is worth more than a polite green light. Dan brought the idea; he needs the truth about it, not validation.
- **The angle comes from the gap.** Refinement isn't wordsmithing the idea — it's finding what the existing coverage misses and aiming there.
- **One video, one promise.** Scoping is mostly deciding what to leave out. Cut material is future-video fuel, not waste.
