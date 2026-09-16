---
name: video-demo-design
description: Design a video's demo code with Dan in an iterative conversation, then build it into a working, viewer-followable companion repo and shot list — choose the codebase, design backwards from the final frame, get Dan's sign-off on the beats, build and verify every checkpoint, and check off the DEMO_CODE_WORKING pipeline stage. Use after `video-develop-idea` returns a GO, or whenever Dan asks "what code should I show", "build the demo for this video", "I don't know where to start with the example", "set up the companion repo", or has a brief/topic but no on-camera code yet. Deciding WHAT the video covers is `video-develop-idea`; title/thumbnail/intro is `video-packaging`; scaffolding the Premiere project folder is `video-project`. This skill produces the code the camera will actually see.
---

# Demo Design

The demo is the proof of the video's promise. Dan's outperformers are "show, don't slide" videos, and the brief from `video-develop-idea` names a promise — but a promise plus a blank editor is where production stalls. The fix is an ordering rule: **never start from the code; start from the last thing on screen** and design backwards until the first beat is obvious.

This is a **design conversation, not an autonomous build**. Dan has to narrate every line of this code on camera — code he didn't shape is code he can't teach. The skill's job is to structure the discussion: propose, hear his reaction, refine, and only build what's been agreed. Never generate the demo in one shot, even when the brief makes the shape seem obvious.

The honest output of this skill is a branch-per-step repo — `main` holds the final code with the full README, and each step of the build lives on its own branch with a README for that step, every branch verified green — plus a shot list Dan can record from.

**Vocabulary rule:** "beat" is production jargon — it belongs in this design conversation, the demo plan, and the shot list, and nowhere a viewer can see. The public repo is a tutorial, and tutorial readers follow **steps**: branch names, README headings, commit messages, and the ladder table all say "step", never "beat". (Dan's call, 2026-07-31, after a repo shipped with beat-named branches.) "Demo code working" is a pipeline gate — don't check it off on code that mostly works.

## Workflow

### Step 1 — Load the promise

Pull the project's brief (`get_brief` on the ContentOS MCP) and extract the promise sentence, the chosen angle, the scope in/out list, and the assumed audience. Also call `get_demo_plan` — if a plan already exists, this session is a continuation: read it, report where things stand (which beats are built and verified, what's open), and pick up from there instead of redesigning. Restate the promise in one line — every demo beat must trace back to it. If there's no brief, ask Dan for the promise in one sentence (or suggest running `video-develop-idea` first if the idea itself is still fuzzy); don't design a demo for a video whose promise is unknown, because "what to show" is unanswerable without "what am I proving".

### Step 2 — Choose the codebase

Default to a **purpose-built public companion repo**, created under `/Users/vega/dev/youtube/` (the home for all video demo repos — not `/Users/vega/youtube/`, which holds Premiere project folders). Dan's real apps are large, private, and unfollowable; the audience's ability to clone the repo and climb through it themselves is part of the promise, and "code along with me" is a differentiator most competitors can't offer because they demo private products.

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

- **One repo, `main` plus one branch per step** — the same shape as a course repo (see `course-demo-design`; Dan's call, 2026-07-31). Each beat from the design maps to a branch named `step-NN-slug` (zero-padded so they sort in video order; slug is one or two words from the step's name): `step-01-assisted`, `step-02-parallel`. Remember the vocabulary rule: the branch says "step" even though the design conversation called it a beat. **When the video follows an external framework with numbered steps or levels, the branch numbers must match the framework's numbers exactly** — a viewer holding the framework's table will read `step-02` as the framework's step 2, and any drift breaks trust. Bridge work between framework steps (a guardrail build, a migration prep) does not get its own branch: it lands as the final commits of the step it exits, because building the bridge is what it takes to leave that step (Dan's call, 2026-07-31). In that case each branch README answers the framework's own three questions: where you are, what the bottleneck is at this step, and what you build to move to the next one. Each branch holds the app as it stands at the **end** of that step, built on the previous branch's tip so history flows forward. When the last step is verified, `main` lands via `git merge --ff-only` from its tip, then one final commit on `main` swaps in the full README — the walkthrough of the whole build. The "just show me the finished code" crowd lands on `main`; the "I'm following along" crowd checks out their step.
- **Each step branch carries its own README** for that step: what this step does, what was built (key files/classes), how to run and verify it, and what changed since the previous branch — with Previous/Next branch pointers. Same format as the section-branch README in `course-demo-design`; each step's README replaces the previous one on that branch.
- **On-camera intermediate states are checked out, not hand-staged.** A beat's starting state is simply the previous step's branch — `git switch` and roll; the shot list records which branch each shot starts from. Manual staging notes (what to delete/comment and how to restore it) are only for moments *inside* a beat, like a line Dan retypes on camera.
- **Every branch lands green.** As each beat is built: the app boots and every test that exists by that beat passes, verified by actually running them — and `main` must run green before the stage closes. A viewer who checks out a broken branch stops trusting every branch. Often the verification command is itself part of the demo — all the more reason it must be trustworthy.
- **Work items where the demo needs them.** If a beat has agents or the viewer picking up tasks, write the backlog into the repo (GitHub issues once published, or a `TODO.md` until then).
- **Publishable from the start**: README with the promise, follow-along instructions, and a video-link placeholder; `.env.example` never `.env`; no secrets in history (they're unremovable later without a rewrite).
- **Don't push to GitHub until Dan says so.** Making the repo public is his call — build locally and offer `gh repo create` at the end.

### Step 5 — Shot list

For each beat, one entry: what's on screen, live-typed vs pre-baked, which branch the shot starts from plus any in-beat manual staging (what to delete/comment before rolling, and how to restore it), the one-line point Dan makes over it, and the known failure points with their fallback. Its canonical home is the saved demo plan (`save_demo_plan`); present it in the conversation too. If the video's project folder exists (from `video-project`), export a copy there as `shot-list.md` for recording day. It's production material, so it never goes in the public repo.

### Supporting footage while the demo is ready

Add B-roll capture notes to the shot list when the explanation benefits from them: starting
branch/application state, the exact action, visible payoff, framing, and output filename.
Capture clean before/after screens and a brief hold around the result while the app is already
set up. Flag full-screen explanations for `video-visual-story`; actual code changes can use
`video-code-animation`. These are useful shots, not a fixed footage quota. Keep the approved
demo-design conversation and build checkpoints intact.

### Step 6 — Close the stage

When — and only when — every beat is verified green, mark the stage complete (`set_pipeline_stage DEMO_CODE_WORKING`) and save the final state of the plan. Then hand off: `video-packaging` reads the plan via `get_demo_plan` — the final frame is the leading thumbnail-concept candidate, the repo is the description link — and if no project folder exists yet, `video-project` scaffolds it.

## Principles

- **It's Dan's demo.** He teaches this code on camera, so he shapes it in discussion — the skill structures the conversation and does the legwork, it doesn't hand him a finished repo to memorize.
- **The demo proves the promise.** Every beat traces to the brief; everything else is cut material for another video.
- **The viewer can follow.** Clone, check out your step, run, green — every branch, not just `main`. If Dan can demo it but a viewer can't reproduce it, it's a magic trick, not a tutorial.
- **Credibility from guardrails, not size.** Real tests in a small app over no tests in a big one.
- **Pre-bake what can fail; live-type what teaches.**
- **One beat, one idea.** A beat that needs two sentences to justify is two beats — or one beat too many.
