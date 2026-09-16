---
name: release-notes
description: >-
  Write release notes from changes between versions, tags, or commits. Use when asked
  to summarize a release or draft a changelog entry. Do not use for a single PR description
  or to publish a release.
---

# Release notes

Explain what changed for the people using the project.

## Gather the changes

- Confirm the start and end of the release range. Ask if the intended range is unclear.
- Read existing release notes to match the project's format and audience.
- Review the diff and commit history. Use PRs or issues for context when available.
- Verify behavior changes in the code. Commit titles alone may be misleading.

## Write the notes

- Lead with the changes readers are most likely to care about.
- Group related work under useful headings, such as Added, Changed, and Fixed.
  Omit empty sections.
- Describe the effect of a change instead of repeating commit messages.
- Combine commits that deliver one change. Skip internal cleanup unless it affects users
  or the release notes are intended for maintainers.
- Make breaking changes easy to find. Give concrete upgrade steps when supported by the repo.
- Link to relevant PRs or issues when their references are verified.
- Do not invent version numbers, release dates, compatibility promises, or migration steps.
- Return a draft or update the requested local file. Publishing is a separate task.

## Writing style

- Use plain words and short bullets. No em dashes.
- Avoid hype and unexplained internal terms.
- Tell the user about missing context or unverified upgrade steps outside the draft.
