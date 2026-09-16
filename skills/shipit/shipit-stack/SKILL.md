---
name: shipit-stack
description: >-
  Choose technology for a new project or a feature that needs a material technical
  decision. Use when Dan asks what to build with, requests a tradeoff, or needs a
  choice about storage, authentication, deployment, or another service.
---

# Stack

Make the choices the next build needs and record why they fit.

## Read the context

Read PRODUCT.md, relevant project files, and recorded preferences.
Use choices already made. An existing build file or established convention usually
answers the question without another conversation.

When starting from an empty project, use the stated purpose and first useful result.
If no PRODUCT.md exists and the request includes planning or building, use shipit-mvp
to create a short initial file. A request for advice alone can stay in the response.

## Match the decision to its effect

- For a cheap implementation choice within scope, use a sensible default and proceed.
- For a choice that changes behavior, compatibility, operating cost, or the agreed
  direction, explain the tradeoff and ask unless the choice is already delegated.
- For "you pick," make a considered choice within the stated constraints and record why.
- Leave choices for later features open until those features need them.

Assess the effect of a dependency, not just whether it is new. A small helper does
not need the same discussion as adding a database or hosted service.

## Make the discussion useful

Derive the questions from this project. Do not run a standard stack questionnaire.
Check deployment constraints before choosing storage when the two depend on each other.
Treat rendering, styling, and asset tooling as separate choices only when each is
unresolved and matters to the next step.

Recommend a default and explain the tradeoff in the question.
Ask one question at a time when the answer changes later choices. Batch independent
choices when that is easier to answer.

Prefer the smallest setup that serves the stated purpose.
If a choice adds unnecessary work, explain the concrete cost once, then respect the
answer. Learning a technology is a valid reason to choose it.
Revisit a settled choice only when the user asks or relevant constraints have changed.

## Record and continue

Record each material decision in PRODUCT.md with its reason and important tradeoff.
For an uncertain or delegated choice, add a concrete reason to revisit it when useful.
A delegated choice was still considered; do not label it "not weighed."

If a decision conflicts with the plan, resolve that conflict before changing the plan.
After a single decision, return to the feature. Do not audit the rest of the stack.
Do not create a separate decisions file when PRODUCT.md can hold the result.

Use plain words and short instructions. No em dashes.
