---
name: shipit-feature
description: >-
  Build and verify the next feature in a shipit project. Use when Dan asks to add,
  implement, or fix something against an existing PRODUCT.md. Keep small changes
  direct and create a feature spec only when it helps coordinate substantial work.
---

# Feature

Build within the agreed scope, verify the result, and leave the project ready
for the next session.

## Read the current plan

Read PRODUCT.md and the relevant code. Read .shipit/open.md if it exists so unfinished
work does not disappear between sessions.
For a new project without PRODUCT.md, use shipit-mvp to record enough to start.
If Dan explicitly asks to skip planning, proceed within the request without creating it.

## Choose the amount of process

For a focused change with clear behavior, work directly from the request.
Do not create a spec or update product notes unless scope, decisions, or current state
actually change. Judge impact rather than line count: a dependency bump or one-line
security change may still need careful verification.

For larger work, outline the change, acceptance criteria, and how to check them.
Keep this in the conversation unless multiple steps or sessions make a saved spec useful.
An optional spec goes in .shipit/specs/ with a descriptive filename. It records the work,
not a second copy of the product plan.

## Resolve scope before building

- Check the request against non-goals, recorded decisions, and the current goals.
- If it changes agreed scope or conflicts with a decision, explain the consequence
  and ask unless Dan already authorized that change.
- An explicit instruction to change an old decision is authorization. Record it
  without asking for the same decision again.
- Use recorded preferences and reasonable defaults for routine implementation choices.
  Use shipit-stack for a material unresolved choice, not every new dependency.
- Respect any additional Stops in PRODUCT.md. Without that section, use these defaults.
- Continue independent work while a required answer is pending.

Mention relevant conflicts and assumptions briefly. Do not narrate a checklist on every run.

## Build and verify

Define expected behavior before implementing it. Choose a check that would catch a
meaningful failure, using the repo's existing commands where possible.
Use shipit-verify if a needed check or convenient entry point is missing.
A small project does not need a custom harness just to run its existing tests.

Implement the change and run focused checks.
For a bug fix, demonstrate the failure before the fix when practical, then show the
regression test passes. For other work, use a negative case or another focused check
when needed to show the test can detect the failure it claims to cover.
Do not require deliberately breaking code for every new check.

Fix failures and rerun relevant checks without asking Dan to debug routine errors.
If a check is wrong, correct it against the acceptance criterion and explain the correction.
Do not weaken the criterion or skip a failing check just to report success.

If repeated attempts produce no new evidence or progress, stop that branch and report
the failure, attempts made, and what is needed next. Do the same for an unavailable
dependency or environment that prevents verification. Continue unrelated work.
Ask before crossing an unresolved scope boundary or a project stop.

Run the appropriate broader checks before finishing. Report anything you could not run.
For a substantial or risky diff, review it for concrete problems using code-review
when available. Focus any security review on risks introduced by the change.
Rerun relevant checks after fixes.

## Review and update

Present one useful batch: what changed, actual check results, evidence needing judgment,
material choices made, and anything blocked or unfinished.
Routine copy and visual changes within the agreed direction belong in this batch.

Distinguish "verified" from "evidence collected, review pending."
Do not mark an unresolved criterion as complete just because a screenshot exists.

Update PRODUCT.md only where the current scope, decisions, or state changed.
Keep current state concise rather than appending a changelog.
If unresolved work must survive the session, save it in .shipit/open.md with a next action.
Remove resolved items; do not copy every review note into it.

Mark a saved spec complete only when its work is complete. It may stay in place or move
to .shipit/specs/done/ if that helps navigation. Supporting files are history, not documents
that must be kept in sync with PRODUCT.md.

Use plain words and short instructions. No em dashes.
