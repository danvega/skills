---
name: shipit-verify
description: >-
  Add or improve checks needed by a current feature. Use when Dan asks to set up
  verification, reduce manual checking, or support a check the project cannot yet run.
  Reuse existing test tools and add a ./verify entry point only when it helps.
---

# Verify

Make it easy to check the behavior being built and report what remains uncertain.

## Start with the current need

Read the feature's acceptance criteria, relevant code, and existing test commands.
Use PRODUCT.md for context if present. Verification alone does not require creating it.

Reuse a working command when it is enough. Add a thin ./verify wrapper when one entry
point or named checks would make repeated work easier. Do not replace working test tools
or build checks for features that do not exist yet.

## Separate three results

- **Verified behavior:** an assertion checks the expected result and fails when it is wrong.
- **Evidence collected:** a screenshot, response, or artifact is ready for review.
  Successful collection does not mean the behavior or design is approved.
- **Judgment pending:** a decision cannot be established by a test. Batch it for review
  unless it must be resolved before dependent work can continue.

Choose checks based on the criterion. A response or rendered page can support both
automated assertions and human review.

Evidence collection should fail when capture fails, the artifact is missing, or a
required assertion fails. Human review can remain pending after successful collection.
Do not force every result into a passing test status.

## Keep commands useful

- Return nonzero for failed assertions, setup failures, or failed evidence collection.
- Avoid interactive prompts. Document any required setup, services, or credentials
  without pretending the check ran when they are unavailable.
- Keep focused checks fast enough for the inner loop.
- If adding ./verify, let it run the configured checks with no arguments and a named
  subset with an argument. An unknown check name should fail clearly.
- Put evidence that needs to survive the session in .shipit/verify/evidence/.
  Make clear which artifacts came from this run so older evidence is not mistaken for new.

Run the changed checks and confirm that an appropriate failure case is detected.
Use a regression case, controlled input, or an isolated test fixture where useful.
Do not mutate unrelated project code merely to demonstrate a red result.

## Fit the review flow

Continue within agreed scope and recorded decisions. Ask before changing either unless
the change or choice is already authorized.
Routine implementation choices and visual review go to the end-of-run batch.

If PRODUCT.md has additional Stops, honor them. Add project-specific stops only when
Dan asks for them or agrees they address a concrete need.
Do not introduce an "anything visual" stop by default.

Repeated unchanged approvals can be a reason to discuss removing an extra stop.
They are not proof the stop has no value. Consider the consequence it protects against,
and change it only with authorization.

## Report the result

List the commands run and their actual results.
Separate verified criteria, evidence awaiting review, and checks that are blocked.
If a check cannot run, explain what is missing and the next useful action.

Use plain words and short instructions. No em dashes.
