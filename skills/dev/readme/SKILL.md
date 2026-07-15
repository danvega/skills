---
name: readme
description: >-
  Write, rewrite, or review a README so it serves its actual reader — structure and emphasis chosen
  by project type (CLI, library, web app/service, monorepo, template/scaffold, internal tool). Use
  whenever the task is creating or improving a README or top-level project docs: "write a README",
  "document this project", "clean up the README", scaffolding a new repo, or prepping a project to
  go public. Do NOT use for API reference docs, CONTRIBUTING guides, changelogs, or writing ABOUT a
  project (blog posts, announcements).
---

# README guidance by project type

A README has one job: get its reader to the thing they came for in under a minute. Who that reader
is depends on the project type — identify the type first, then weight the sections accordingly.

## Ground rules (any type)

- **Open with one plain sentence saying what the project is and who it's for.** If the name plus
  the first sentence don't orient a stranger, nothing below will.
- **Verify every command against the repo before writing it.** Read package.json scripts, the
  build file, the Makefile — don't infer install/run commands from convention. A README that lies
  about `npm run dev` costs more trust than no README at all.
- **Document what exists, not what's planned.** Check that every documented feature, flag, and
  endpoint is actually in the code. Aspirational items go in a clearly labeled roadmap section or
  nowhere.
- **No hype.** Cut "blazingly fast", "powerful", "simple yet flexible" — show a code sample or a
  number instead and let the reader judge.
- **Skip the ritual sections** — table of contents, badge walls, emoji headers, boilerplate
  Contributing/License prose — unless the project's size and audience earn them. A 60-line README
  doesn't need a ToC.
- **Match length to the project.** A weekend CLI needs 30 lines; a framework might need 200 plus
  links out to real docs. When a section grows past a screen, that's a sign it wants to be a
  separate doc the README links to.

## Writing style

- Use simple, direct language. Prefer the short word: "use" over "utilize", "run" over "execute".
- Keep sentences short, one idea each. If a sentence needs three commas, split it.
- No em dashes. Use a period, a comma, or parentheses instead.
- Be concise. Every line should earn its place. If a sentence still reads fine with a word
  removed, remove the word.

## CLI tool

Lead with installation and a single representative command. Prioritize:
- Install one-liner (npm/brew/cargo/pip/go install).
- A "common commands" table or list with one-line descriptions.
- Flags and options, or a pointer to `--help`.
- Exit codes only if scripting against them matters.

## Library / package

The reader is a developer deciding whether to depend on you. Prioritize:
- Install command for the relevant package manager.
- A minimal import + call example that returns something — runnable as-is, not pseudocode.
- API surface overview (link to full reference rather than inlining it).
- Version/compatibility notes (language version, peer dependencies).

## Web app / service

The reader wants to run it locally or deploy it. Prioritize:
- Prerequisites (runtime, database, external services).
- Environment variable table: name, required/optional, description, example.
- Local dev startup sequence (install, migrate, seed, run) — verified end to end.
- How to run tests.
- Deployment pointer if relevant.

## Monorepo

Keep the root README high-level. Prioritize:
- What the repo contains (package/app list with one-line descriptions).
- Shared tooling and setup (workspace install, build orchestration).
- Pointers to per-package READMEs rather than documenting each package at the root.

## Framework / scaffold / template

Prioritize:
- What you get out of the box.
- How to start a new project from it.
- Where to customize.

## Internal / team project

External polish matters less; onboarding speed matters more. Prioritize:
- How to get a working dev environment fast.
- Who owns it / where to ask questions.
- Links to runbooks, dashboards, and deeper internal docs.

## Review pass

Before finishing, reread as the target reader with zero context: can they say what this project is
in one sentence, and did the quickstart work on the first try? If the README already existed,
preserve any hard-won operational notes (weird setup steps, known issues) — those are the most
valuable lines in it, even when they're ugly.
