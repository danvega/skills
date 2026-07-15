# CLAUDE.md — authoring conventions for this repo

This is Dan Vega's personal skills repository. When creating or editing skills here,
follow these rules.

## Two layers, kept separate

- **Knowledge skills** (`skills/spring-boot-4/`, future `spring-ai/`, `java/`) are
  auto-discovered by description match. They encode framework/language deltas.
- **Workflow skills** (`skills/blog/`, `skills/youtube/`) are processes that drive
  a repeatable task end to end (drafting a post, generating video ideas).
- Don't mix the two in one folder; their descriptions optimize for different things.

## Every knowledge skill

- `SKILL.md` is a **router**, not an essay. Body under ~150 lines. Route by task to
  `reference/*.md` files.
- Reference files are **one level deep** — never `SKILL.md → ref → ref`.
- Encode the **delta only**. Assume the model knows Spring; tell it what changed in
  4.x/7.x and what the current idiom is. Don't re-explain a `@RestController`.
- Put deprecated 3.x patterns in a collapsed `<details>` "Legacy" block so the
  current path stays clean and the skill doesn't rot on a date.
- State the version baseline explicitly (Boot 4.0+, Framework 7.0+, Java 25+).
- Include real gotchas (the exceptions you actually hit), not just happy-path code.

## The description field

This is what discovery runs on. Write it third-person, lead with what it does +
when to use it, name concrete triggers (the annotations, the feature names), and
add an explicit "Do NOT use for…" pointing at the sibling skill that does cover it.

## Before committing

This is a plain skills repo (no marketplace/plugin packaging). Sanity-check that every
skill folder has a `SKILL.md` with valid `name` and `description` frontmatter, and that
the README's skill list matches what's actually in `skills/`.
