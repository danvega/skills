---
name: shipit-prototype
description: >-
  Explore a product's uncertain screen or interaction before investing in implementation.
  Use when Dan asks for a mockup, wants to compare visual directions, or needs to resolve
  a UI question. Skip when an established pattern or a working first version is enough.
---

# Prototype

Answer a specific design question with the smallest useful prototype.
A prototype can confirm the current plan or reveal a change worth making.

## Decide whether it helps

Read the request, PRODUCT.md, and existing visual patterns.
A UI alone is not a reason to run a design session.
Skip this step when the next screen has a clear default, and Dan has not requested a mockup.

Choose the screen or interaction carrying the uncertainty.
Do not automatically exclude a login or settings screen if that is where the real question is.
This skill can run before the first build or later when a new question appears.

If the request includes planning a new project and PRODUCT.md is missing, use shipit-mvp
to record a short initial plan. For a standalone mockup request, use the supplied context
without requiring a product document.

## Build the smallest useful comparison

- State the question the prototype should answer.
- Use real field names and realistic values, including long or dense content.
- Consider empty, loading, error, and crowded states where they affect the question.
- Carry relevant non-goals into the design so it does not imply unrequested features.
- Reuse an established visual direction unless Dan asks to explore a change.
- Show alternatives when there is a real choice to compare. Do not require several
  versions when one experiment answers the question.

Use an available design tool or a small HTML prototype, according to the task.
Keep the implementation effort proportional to what needs to be learned.
If handing off to another tool, provide a self-contained prompt with the question,
content, constraints, and desired output.

## Review and record

Show the result and explain what it confirms or leaves uncertain.
Ask only for the judgment needed to choose a direction.
If it suggests a change to the agreed scope, get that change resolved before implementing it.

Record the chosen direction and reasons in PRODUCT.md when it exists.
Include useful patterns for later screens, such as recurring components and state behavior.
A confirmed plan is a valid result. Do not change goals just to justify the prototype.

Save useful artifacts under .shipit/prototype/ when they need to survive the session.
Keep older rounds as history without treating their code or images as current requirements.
PRODUCT.md holds current decisions. No deletion or archive ceremony is required.
Return to the build when the question is answered and the request includes implementation.

Use plain words and short instructions. No em dashes.
