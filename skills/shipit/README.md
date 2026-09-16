# shipit

My process for building demos, small tools, and products without turning setup into
the main job.

1. **Decide enough to start.** Identify the first useful result and record the boundaries.
2. **Build something you can verify.** Use focused checks and fix failures as you go.
3. **Review and update.** Show the result, resolve open judgments, and keep the plan current.

The skills support these actions. They are not seven required stages.

## Start where you are

- **The idea is unclear:** use `/shipit-shape` to find the smallest useful version.
- **The idea is clear:** use `/shipit-mvp` to create a short initial `PRODUCT.md`.
- **Ready to build:** use `/shipit-feature`. It fills in missing planning or checks only
  when the work needs them.
- **A small fix:** work directly from the request. No feature spec is required.

When the request includes building, continue after planning without another approval round.
When the request is only for advice or a plan, return that result.

This workflow is designed for new projects and continued work in projects that use
`PRODUCT.md`. Adopting an unrelated existing codebase is a separate task.

## Match the process to the project

| Mode | Enough to start | Add only when useful |
| --- | --- | --- |
| Demo | The teaching point, audience, visible result, and relevant boundaries | A rehearsal or check of the demonstrated behavior |
| Small project | A focused outcome, known defaults, and a short PRODUCT.md | A stack decision or prototype that resolves real uncertainty |
| Product | Initial goals, boundaries, and decisions needed for the first feature | More planning as features and operating needs become concrete |

A demo can be valuable just for teaching. A personal tool can be valuable to one user.
Neither needs to justify becoming a larger product.

## The working flow

```text
unclear idea -> shipit-shape
                     |
clear idea ----------+
                     v
                 shipit-mvp
           initial PRODUCT.md
                     |
                     v
                shipit-feature <--------------------+
                     |                              |
                     +-> shipit-stack, if needed    |
                     +-> shipit-prototype, if useful|
                     +-> shipit-verify, if needed   |
                     |                              |
                     v                              |
             build, check, review                   |
                     |                              |
                     +-> update current state ------+
```

Create `PRODUCT.md` early. Stack choices and prototypes refine it when they are needed.
Do not require those sessions to finish before recording the initial plan.

## The skills

| Skill | Purpose |
| --- | --- |
| [shipit-shape](./shipit-shape/SKILL.md) | Clarify an idea and recommend building, narrowing, or setting it aside. Stop asking when enough is known. |
| [shipit-mvp](./shipit-mvp/SKILL.md) | Record the purpose, first useful result, boundaries, decisions, and current state. |
| [shipit-stack](./shipit-stack/SKILL.md) | Resolve a material technical choice and record its reason. Use known defaults for routine choices. |
| [shipit-prototype](./shipit-prototype/SKILL.md) | Answer an uncertain design question. Skip when an established pattern or first working version is enough. |
| [shipit-verify](./shipit-verify/SKILL.md) | Add the checks the current feature needs. Reuse existing tools before introducing a wrapper. |
| [shipit-feature](./shipit-feature/SKILL.md) | Build within scope, verify behavior, present a review batch, and update current state. |
| [shipit-retro](./shipit-retro/SKILL.md) | Propose a focused process improvement when there is evidence of friction. Run on demand. |

## The files

`PRODUCT.md` holds current product scope and decisions. Supporting files hold work and history.
Use the sections and supporting files the project needs.

| File | When useful |
| --- | --- |
| `PRODUCT.md` | Current purpose, goals, non-goals, decisions, state, and any additional project stops |
| `.shipit/shape/brief.md` | Shaping context that must survive a handoff before it reaches PRODUCT.md |
| `.shipit/specs/*.md` | A substantial feature plan spanning multiple steps or sessions |
| `.shipit/prototype/` | Mockups and design experiments worth retaining |
| `.shipit/verify/evidence/` | Artifacts from checks that need review |
| `.shipit/open.md` | Unresolved work with a next action, pruned as items are resolved |
| `.shipit/retro/findings.md` | Process observations worth checking in a later session |

Do not create empty supporting files. Keep historical notes without maintaining them
as duplicate plans. A finished spec may stay in place or move to `.shipit/specs/done/`.
No automatic deletion is required.

## Where the human belongs

Continue within the agreed scope and recorded decisions. Ask before changing either
unless the change or choice is already authorized. "You pick" permits a considered
choice within the stated constraints.

Use known preferences and reasonable defaults for routine implementation choices.
Batch visual review, evidence, and minor choices at the end. A UI does not automatically
require a design session or a mid-build stop.

An optional `Stops` section in `PRODUCT.md` adds project-specific reasons to pause.
Without it, the defaults above apply. Continue independent work while an answer is pending.

Verification reports three distinct results: behavior verified, evidence collected,
and judgment pending. Failed evidence capture is a failure; successful capture is
not approval. If repeated attempts produce no progress or the environment blocks a
check, report what is needed rather than looping indefinitely.

## Improve it through use

Run `/shipit-retro` when the process gets in the way or a completed run reveals a useful lesson.
Prefer removing unnecessary work to adding rules. Try the change on a relevant task
and judge it by the result, including how often Dan had to intervene.
