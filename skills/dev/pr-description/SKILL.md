---
name: pr-description
description: >-
  Write or update a pull request title and description from a code diff. Use when asked
  to describe a PR, summarize branch changes for reviewers, or prepare a PR draft.
  Do not use for code review or release notes.
---

# Pull request description

Help a reviewer understand the problem, the change, and how it was checked.

## Read the changes

- Read the repo's PR template and contribution rules, if present.
- Use the requested PR or diff. For a branch, confirm the base and read the full branch diff.
- Check nearby code and linked issues when needed to understand the reason for a change.
- Ask for the intended comparison if it cannot be determined from the repo.

## Write the draft

- Give the PR a short title that describes the resulting behavior.
- Start with the problem and explain what changes for the user or developer.
- Include a before and after example when it makes the change easier to understand.
- Mention technical details, breaking changes, or rollout steps only when they matter.
- Follow the repo's template. Without one, use a brief description and a testing section.
- Report tests actually run and their results. Label suggested checks and unverified claims.
- Keep the description focused on the final diff. Leave out abandoned approaches and chat history.
- Return the draft unless the user asks to create or update the PR.

## Writing style

- Use plain words and short sentences. No em dashes.
- Scale the detail to the change. A small fix may need only a few sentences.
- Do not invent motivation, issue numbers, test results, or performance claims.
