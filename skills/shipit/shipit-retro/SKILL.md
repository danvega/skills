---
name: shipit-retro
description: >-
  Review how the shipit process worked and propose a focused improvement. Use when Dan
  asks for a retro, says the process got in the way, or wants to learn from a completed
  build. Do not run automatically after every feature or use for product code review.
---

# Retro

Find one useful improvement to the process or say no change is needed.

## Read the evidence

Use the available conversation, PRODUCT.md, relevant .shipit/ notes, diffs, and check results.
Do not claim to have reviewed a session or run a command you cannot access.

Look for a concrete gap between the intended process and what happened:

- Questions that repeated known information or delayed useful work.
- Scope changes or decisions of the agent failed to surface.
- Checks that passed while the behavior was wrong.
- Repeated failures that did not lead to a new diagnosis.
- Work or review findings lost between sessions.
- Steps repeatedly skipped because they cost more than they helped.

Use counts when available, but a specific example can establish a problem.
Dan's report of friction is useful evidence. Trace it to an instruction or handoff
rather than dismissing it because it happened once.
Repeated approvals suggest a stop may deserve review; they do not prove it is unnecessary.

## Propose a focused change

Prefer the smallest change that addresses the cause.
Delete redundant instructions or relax an unnecessary gate before adding another rule.
Do not generalize one unusual incident into a requirement for every project.

Give the file, current instruction, proposed replacement, and supporting evidence.
A correction may touch several files if they describe the same handoff or rule.
Keep that one coherent change rather than preserving contradictions to meet a file quota.

Propose the edit for review. Apply it when Dan asks to make the change.
If there is no supported improvement, say so without inventing one.

## Keep the follow-up light

Do not create a retro report by default.
If an unresolved pattern needs to survive the session, add a short entry to
.shipit/retro/findings.md with the evidence and what to watch for next.
Update or remove resolved entries. This is supporting process history, not product scope.

For a changed workflow, suggest a relevant small task to try next and what improvement
to look for. Distinguish a review of the instructions from an actual workflow trial.

Use plain words and short instructions. No em dashes.
