---
name: bug-repro
description: >-
  Reproduce a reported bug and capture it in a regression test, then apply a focused fix
  when requested. Use for unexpected behavior, a failing case, or a bug report that needs
  investigation. Do not use for general code review or new features.
---

# Reproduce a bug

Make the failure observable before changing the code.

## Find the failure

- Read the report, relevant code, and existing tests.
- Identify the input, expected result, and actual result. Ask only for missing details
  that prevent reproduction.
- Use the repo's existing test tools and setup commands.
- Reduce the report to the smallest case that still shows the bug.
- If the bug cannot be reproduced, report what you tried and what evidence is missing.
  Do not present a suspected cause as a confirmed one.

## Capture and fix it

- Add a regression test that checks the expected behavior. Run it before the fix.
- Confirm it fails because of the reported bug, not a setup error or unrelated failure.
- If an automated test is impractical, provide repeatable steps and the observed result.
- For a reproduction-only request, stop after documenting the failure.
- When a fix is requested, change only what is needed to address the cause.
- Run the regression test again, then the relevant existing tests.
- Keep the test focused on behavior so it still helps after a refactor.

## Report the result

- Explain the cause, the reproduction, and any fix in plain language.
- Include the commands run and their results, plus anything still unverified.
- Keep instructions short and in order. No em dashes.
