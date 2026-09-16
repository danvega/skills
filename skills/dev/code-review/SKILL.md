---
name: code-review
description: >-
  Review a pull request, diff, or selected code for actionable bugs and regressions.
  Use when asked to review code or check changes before merging. Do not use to write
  a PR description or perform a broad style cleanup.
---

# Code review

Find problems that matter and give the author enough evidence to act.

## Review the code

- Confirm the requested scope. For a branch or PR, identify the base and read its diff.
- Read the repo's review rules and enough surrounding code to understand each change.
- Follow relevant callers, configuration, and tests before calling something a bug.
- Focus on incorrect behavior, broken compatibility, data loss, and security issues.
- Check whether tests cover the changed behavior and meaningful failure cases.
- Tie style feedback to an explicit project rule or a concrete problem it causes.
- Use a focused test or reproduction when it would resolve uncertainty.
- Review without editing files unless the user also asks for fixes.

## Report findings

- Put the most serious findings first. Include only issues supported by the code or evidence.
- For each finding, give a short title, a file and line reference, the triggering case,
  and the consequence. Suggest a fix when it is clear.
- For a diff review, focus on problems introduced by the change. Separate older issues
  if they are relevant to the request.
- Do not fill a quota. If there are no actionable findings, say so.
- Note what was checked and any important gaps. Keep open questions separate from findings.
- Use plain language and short paragraphs. No em dashes.
