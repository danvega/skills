# Authoring conventions

This is Dan Vega's personal skills repository. Keep skills focused on the choices,
conventions, and lessons that improve a real task.

## Organization

- `skills/dev/`: general development tasks.
- `skills/shipit/`: planning, building, and reviewing demos or products.
- `skills/spring/`: framework guidance, grouped by release or product.
- `skills/blog/`, `skills/newsletter/`, `skills/podcast/`, `skills/video/`, and
  `skills/contentos/`: personal content workflows.

Framework guidance should focus on version-specific changes and gotchas.
Workflow skills should describe the outcome and the decisions needed to reach it.

## Naming and discovery

- Match the folder name to the frontmatter `name`.
- Use lowercase letters, numbers, and hyphens.
- Keep pipeline prefixes such as `shipit-`, `blog-`, `newsletter-`, `video-`, and `contentos-`.
- Podcast workflows may use the show name, such as `spring-office-hours-`.
- General dev skills stay unprefixed, such as `readme` and `code-review`.
- Framework skill names describe the capability, such as `jackson-3`.

A description says what the skill does and when to use it.
Add an exclusion when it prevents overlap with another skill that actually exists.
Keep descriptions under 1,024 characters and omit angle-bracket placeholders.

Use a folded YAML string so punctuation does not break the frontmatter:

```yaml
---
name: example-skill
description: >-
  Describe the task this skill handles and when it applies.
---
```

## Writing instructions

- Use plain words and short instructions. No em dashes.
- Include only guidance that changes how the agent should do the task.
- Keep small tasks small. Avoid quotas, repeated confirmations, and mandatory steps
  that do not help the requested work.
- Use supporting references for substantial detail. A short skill can be self-contained.
- State framework version baselines and distinguish current patterns from legacy examples.
- Preserve useful operational notes and the user's existing authorization.
- For personal workflows, make required paths, tools, accounts, and assets clear.
- Keep source attribution and licenses with vendored resources.

## Before committing

- Check each skill's YAML, name, description, and referenced local files.
- Keep the README catalog aligned with the skills that exist.
- Check that install examples point to real folders.
- Exclude local settings, dependencies, and generated output.
- Validate changed scripts with relevant checks. Documentation checks do not prove a
  media or publishing workflow works end to end.
