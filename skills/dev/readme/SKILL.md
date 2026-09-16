---
name: readme
description: >-
  Write, update, or review a project README. Choose the content based on the project and its
  readers. Use when the task includes creating or improving a README. Do not use for API
  reference docs, contributing guides, changelogs, or blog posts.
---

# README guidance by project type

A README should help readers understand the project and get started. Identify who will read it
and what they need first. Use the project guidance below where it fits.

## Ground rules

- Open with one sentence saying what the project does and who it is for.
- Check commands against the repo's scripts and build files. Do not guess setup commands.
- Describe features that exist. Label planned work clearly if it needs to be included.
- Preserve useful setup notes, known issues, and project conventions when editing a README.
- Include only sections that help the reader. Add a table of contents when it helps navigation.
- Keep small projects brief. Link to separate docs for detailed topics.

## Writing style

- Use plain words, such as "use" instead of "utilize" and "run" instead of "execute".
- Keep sentences short and focused on one idea.
- No em dashes. Use a period, a comma, or parentheses instead.
- Give direct steps in the order the reader needs them. Avoid nested instructions.
- Remove repetition, filler, and claims like "blazingly fast" or "powerful".

## CLI tool

Lead with installation and one useful command.

- Show how to install the tool.
- List common commands with short descriptions.
- Explain key options or point to `--help`.
- Include exit codes when readers need them for scripts.

## Library / package

Help developers decide whether to use the package and make their first call.

- Show the install command.
- Give a small, runnable example with its expected result.
- Summarize the main API and link to the full reference if available.
- State supported versions and required dependencies.

## Web app / service

Help readers run the app locally.

- List required runtimes, databases, and services.
- Explain required settings and environment variables. Use safe example values.
- Show setup and startup commands in order.
- Show how to run tests.
- Link to deployment instructions when relevant.

## Monorepo

Keep the root README focused on the repo as a whole.

- List packages and apps with short descriptions.
- Explain shared setup and build commands.
- Link to each package's README for details.

## Framework / scaffold / template

- Explain what is included.
- Show how to start a new project.
- Point out where to customize it.

## Internal / team project

- Show how to set up a working development environment.
- Identify the owner and where to ask questions, if known.
- Link to relevant runbooks, dashboards, and team docs.

## Review pass

- Check that a new reader can understand the project and find the first useful step.
- Try the quickstart when the environment allows it. Tell the user what you could not verify.
- Check that links and file paths point to the intended pages or files.
- Remove em dashes and simplify any instructions that are hard to follow.
