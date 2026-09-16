---
name: prepare-pull-request
description: Publish or update an authorized Issue implementation as a Pull Request and validate its checks through maintainer review. Use after implementation, without implying merge authorization.
---

# Prepare Pull Request

## Purpose

Turn a completed, locally validated Issue implementation into a high-quality GitHub Pull Request and drive its automated checks to green.

## Preconditions

- Implementation is complete on a dedicated branch.
- The branch corresponds to a GitHub Issue.
- The user has authorized publication; reuse prior authorization and respect
  explicit restrictions. Otherwise prepare the PR text locally without pushing.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md) and the related GitHub Issue.
2. Inspect `git status` and the complete diff against `main`.
3. Ensure the diff contains no unrelated changes, secrets, generated junk, or debug artifacts.
4. Re-run relevant local checks when necessary.
5. Verify the acceptance criteria one by one.
6. For significant architectural changes, ensure [senior-architecture-review](../senior-architecture-review/SKILL.md) has reviewed the final diff.
7. Create a small number of coherent Conventional Commits when commits are authorized.
8. Push the feature branch.
9. Create or update the existing PR targeting `main` using the
   [repository template](../../../.github/pull_request_template.md); do not duplicate it.
10. Include `Closes #<issue-number>`, verify the linked Issue and keep it open
    until merge. Follow [CONTRIBUTING.md](../../../CONTRIBUTING.md) for dependent
    branches, including retargeting and reviewing the diff after prerequisite merges.
11. Explain why the change exists, not only what the diff contains.
12. Include screenshots for visible UI changes when practical.
13. Monitor required GitHub checks.
14. Inspect failures and fix their root cause when caused by the change.
15. Push fixes and repeat until required checks are green.
16. Inspect Sonar and security results when available.
17. Address new justified findings or clearly identify findings requiring maintainer judgment.
18. Review final `git status` and the complete PR diff, including fixes after CI.

## PR expectations

The PR should cover:

- Summary
- Why
- Changes
- Testing
- Quality and security impact
- Screenshots when applicable
- Architectural notes when relevant
- Known limitations / follow-up

## Rules

- Do not bypass branch protections.
- Do not downgrade checks merely to obtain a green PR.
- Do not silently dismiss Sonar/security findings.
- Do not merge or enable auto-merge without explicit user authorization for that PR.
- Sonar currently analyzes `main` after merge. Do not claim PR analysis when it
  did not run, or merge without authorization to obtain a Sonar result. Review
  available results against the actual analyzed revision.

## Completion

Report:

- Issue number and URL;
- branch;
- PR number and URL;
- required checks status;
- coverage impact when available;
- Sonar/security status;
- remaining concerns.

End with:

`PR ready for maintainer review.`
