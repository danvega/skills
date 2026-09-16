---
name: code-tour
description: >-
  Explain how a repository or feature works by tracing a real request, command, or event
  through the code. Use for codebase walkthroughs, onboarding, or questions about where
  behavior is implemented. Do not use for a code review or a README rewrite.
---

# Code tour

Help a developer follow one useful path through the project.

## Choose a path

- Start with the feature or behavior the user asked about.
- For a general tour, inspect the README and entry points, then choose a representative flow.
- Say which flow you chose and what it demonstrates.

## Follow the code

- Trace the entry point through the main logic to its output or side effect.
- Follow actual calls and wiring. Do not assume behavior from file or class names alone.
- Explain relevant configuration, storage, and external services where they enter the flow.
- Include the tests that demonstrate the behavior, if present.
- Distinguish what the source shows from what you verified by running it.

## Give the tour

- Open with a short explanation of the project or feature.
- Present the flow in order with links to real files and useful line references.
- Explain each stop's role and why it matters. Skip a full directory listing.
- Add a small diagram only when it makes the flow easier to follow.
- End with the best starting point for the user's next change or investigation.
- Keep the tour in the response unless the user asks for a saved document.
- Use plain words and short steps. No em dashes.
