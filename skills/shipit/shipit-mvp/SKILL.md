---
name: shipit-mvp
description: >-
  Create or refine a short PRODUCT.md for a new demo, small project, or product.
  Use when Dan asks to define an MVP, scope a first version, or record the plan before
  building. Use shipit-feature for routine feature work in an existing shipit project.
---

# MVP

Create PRODUCT.md early and refine it as the project becomes clearer.
It holds current product scope and decisions. Supporting files hold work and history.

## Start with what is known

- Read the request, recorded preferences, and any existing PRODUCT.md.
- Use relevant shaping or prototype notes if present. Resolve conflicting context
  before treating an older note as current.
- Do not require a separate shaping, stack, or design session.
- If PRODUCT.md already covers the request, use it and continue. Refine it when Dan
  asks to change the plan; do not overwrite settled decisions by accident.
- For an unrelated existing codebase, avoid inventing a product plan from the code.
  Ask only if the requested scope cannot be established.

## Record enough to start

- **Purpose:** who this serves and the problem or idea it addresses.
- **First useful result:** behavior someone can see or use, with plain acceptance criteria.
- **Non-goals:** meaningful boundaries and their reasons. Label them "not now" or
  "outside this project's purpose" when that distinction helps. There is no minimum count.
- **Decisions:** choices already made, with reasons. Separate unresolved questions
  from decisions and stated assumptions.
- **Current state:** what works, what is in progress, and the next useful step.

A demo may need only a few lines. A product may need more goals and context.
Ask about likely scope creep only when the boundary is unclear.
Do not invent exclusions or features to fill a template.

## Resolve only what blocks the first build

Use known preferences and existing project conventions.
For cheap choices within scope, state the assumption and proceed.
Use shipit-stack when a choice has a material effect on behavior, compatibility,
operating cost, or the agreed direction.

"You pick" authorizes a considered choice within the request, including choices that
support an acceptance criterion. Record the choice and reason. Ask again only if new
information falls outside that authorization.

A UI does not require a prototype. Use shipit-prototype when a layout or interaction
is uncertain enough that exploring it would help. Otherwise build a first version
using the known direction and show it for review.

## Interruptions

By default, continue within the agreed scope and decisions. Ask before changing either
unless Dan has already authorized the change or delegated that choice.
Ask about unresolved details only when guessing would materially change the result.
Routine implementation choices and visual review go in the final batch.

An optional Stops section records additional project-specific reasons to pause.
Its absence uses these defaults; it does not require stopping on every decision.

## Keep the file useful

Use only the sections the project needs. Update current state instead of appending a log.
Supporting notes can stay in .shipit/ as history, but should not duplicate current decisions.
If the user asked to build, continue with shipit-feature once enough is known.
If the user asked only for a plan, return the plan.

Use plain words and short instructions. No em dashes.
