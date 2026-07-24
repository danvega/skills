---
name: video-demo-design
description: Design a video's demo code with Dan in an iterative conversation, then build it into a working, viewer-followable companion repo and shot list — choose the codebase, design backwards from the final frame, get Dan's sign-off on the beats, build and verify every checkpoint, and check off the DEMO_CODE_WORKING pipeline stage. Use after `video-develop-idea` returns a GO, or whenever Dan asks "what code should I show", "build the demo for this video", "I don't know where to start with the example", "set up the companion repo", or has a brief/topic but no on-camera code yet. Deciding WHAT the video covers is `video-develop-idea`; title/thumbnail/intro is `video-packaging`; scaffolding the Premiere project folder is `video-project`. This skill produces the code the camera will actually see.
---

# Demo Design

The demo is the proof of the video's promise. Dan's outperformers are "show, don't slide" videos, and the brief from `video-develop-idea` names a promise — but a promise plus a blank editor is where production stalls. The fix is an ordering rule: **never start from the code; start from the last thing on screen** and design backwards until the first beat is obvious.

This is a **design conversation, not an autonomous build**. Dan has to narrate every line of this code on camera — code he didn't shape is code he can't teach. The skill's job is to structure the discussion: propose, hear his reaction, refine, and only build what's been agreed. Never generate the demo in one shot, even when the brief makes the shape seem obvious.

The honest output of this skill is a single-branch repo — the final code, running green, with a README that walks the reader through how it was built — plus a shot list Dan can record from. "Demo code working" is a pipeline gate — don't check it off on code that mostly works.

## Workflow

### Step 1 — Load the promise

Pull the project's brief (`get_brief` on the ContentOS MCP) and extract the promise sentence, the chosen angle, the scope in/out list, and the assumed audience. Also call `get_demo_plan` — if a plan already exists, this session is a continuation: read it, report where things stand (which beats are built and verified, what's open), and pick up from there instead of redesigning. Restate the promise in one line — every demo beat must trace back to it. If there's no brief, ask Dan for the promise in one sentence (or suggest running `video-develop-idea` first if the idea itself is still fuzzy); don't design a demo for a video whose promise is unknown, because "what to show" is unanswerable without "what am I proving".

### Step 2 — Choose the codebase

Default to a **purpose-built public companion repo**. Dan's real apps are large, private, and unfollowable; the audience's ability to clone the repo and climb through it themselves is part of the promise, and "code along with me" is a differentiator most competitors can't offer because they demo private products.

- **Small enough to read in ~10 minutes.** One domain concept, a REST API, a service layer, a real test suite. If a viewer can't hold the whole app in their head, the app is stealing attention from the topic.
- **Real enough to be credible.** Credibility comes from the guardrails — an honest test suite, a `./mvnw verify` loop, CI, review gates — not from codebase size. A tiny app with real verification beats a big app with none.
- **New Spring projects start from start.spring.io** with the channel's current defaults (latest stable Boot, current Java LTS-or-later Dan uses, Maven), so viewers can reproduce the starting point exactly.
- An **existing public sample repo** is fine when it already fits the beats — reuse beats rebuild.
- The **private/real app appears only as a cameo** ("here's the same thing running on my real codebase") — never as the primary demo surface.

### Step 3 — Design backwards, together

Work through this order, but as a conversation — present each piece as a proposal with the reasoning, and let Dan push back before moving to the next. Where a choice is genuinely open (domain for the sample app, which feature to build live), offer 2–3 options with a recommendation rather than deciding silently.

1. **Final frame first.** What result, on screen, makes the promise undeniable? Write it as a description of a single screen.
2. **Before-state second.** What starting point makes the contrast visible? The distance between these two states is the video.
3. **Beats between.** The 3–5 code states that connect before to after. Each beat maps to one scope item from the brief — run the check in both directions: anything demoed that's off-promise gets cut; anything promised with no beat gets one or gets descoped from the brief.
4. **Pre-baked vs live, per beat.** Pre-bake anything that can fail or takes longer than ~30 seconds to happen on camera (cooking-show rule) — a live failure kills a take, pre-baked code doesn't. Type live only where *watching it happen* is the point of the beat.

**This step ends with Dan's sign-off on the beat list.** Expect iteration — a beat list that survives contact with Dan unchanged usually means he hasn't really engaged with it yet, so invite the pushback ("which beat feels wrong?") rather than asking yes/no. Do not start building until he's agreed; a demo built on an unapproved design is rework, not progress.

Once he signs off, persist the design to the project with `save_demo_plan` (slug, repo path once it exists, and the plan as markdown: codebase choice with the why, final frame, the beats table with status, decisions and gotchas, draft shot list, open items). The design conversation happened in chat and is gone next session — the saved plan is what makes the work resumable and what `video-packaging` reads later.

### Step 4 — Build and verify

Only after the design is agreed. Build beat by beat, in recording order, and check in as each beat lands — show what was built, how it was verified, and what the next beat is, so Dan can course-correct before the repo hardens around a wrong turn. He may want to build some beats himself; take the supporting role there (review, verify) rather than racing ahead.

After each beat lands (and after any decision that changes the plan), update the saved plan via `save_demo_plan` — mark the beat's status, record new gotchas and decisions. The plan is a living document: by recording day it has become the shot list.

- **One repo, one branch, final code only.** No per-beat tags or branches — `main` holds the finished state, and the README carries a walkthrough section that mirrors the beat list, so a viewer reads how the code got here in the order Dan builds it on camera. Beats are a design and recording structure, not a git structure.
- **On-camera intermediate states are staged, not checked out.** Where a beat shows an earlier state (a file that doesn't exist yet, a block not yet written), Dan produces it at recording time by temporarily deleting/commenting — the shot list records exactly what to remove and how to restore it.
- **Every beat lands green.** As each beat is built: the app boots and the tests pass, verified by actually running them — and the final state on `main` must run green before the stage closes. Often the verification command is itself part of the demo — all the more reason it must be trustworthy.
- **Work items where the demo needs them.** If a beat has agents or the viewer picking up tasks, write the backlog into the repo (GitHub issues once published, or a `TODO.md` until then).
- **Publishable from the start**: README with the promise, follow-along instructions, and a video-link placeholder; `.env.example` never `.env`; no secrets in history (they're unremovable later without a rewrite).
- **Don't push to GitHub until Dan says so.** Making the repo public is his call — build locally and offer `gh repo create` at the end.

### Step 5 — Shot list

For each beat, one entry: what's on screen, live-typed vs pre-baked, how to stage the beat's starting state (what to delete/comment before rolling, and how to restore it), the one-line point Dan makes over it, and the known failure points with their fallback. Its canonical home is the saved demo plan (`save_demo_plan`); present it in the conversation too. If the video's project folder exists (from `video-project`), export a copy there as `shot-list.md` for recording day. It's production material, so it never goes in the public repo.

### Step 6 — Close the stage

When — and only when — every beat is verified green, mark the stage complete (`set_pipeline_stage DEMO_CODE_WORKING`) and save the final state of the plan. Then hand off: `video-packaging` reads the plan via `get_demo_plan` — the final frame is the leading thumbnail-concept candidate, the repo is the description link — and if no project folder exists yet, `video-project` scaffolds it.

## Principles

- **It's Dan's demo.** He teaches this code on camera, so he shapes it in discussion — the skill structures the conversation and does the legwork, it doesn't hand him a finished repo to memorize.
- **The demo proves the promise.** Every beat traces to the brief; everything else is cut material for another video.
- **The viewer can follow.** Clone, run, green — with a README walkthrough that retraces the build. If Dan can demo it but a viewer can't reproduce it, it's a magic trick, not a tutorial.
- **Credibility from guardrails, not size.** Real tests in a small app over no tests in a big one.
- **Pre-bake what can fail; live-type what teaches.**
- **One beat, one idea.** A beat that needs two sentences to justify is two beats — or one beat too many.
