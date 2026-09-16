## Summary

<!-- What problem does this solve, for whom, and why now? Link the task/issue. -->

Closes #<!-- Required: existing GitHub task issue number. -->

Task: <!-- Link TASKS/NNN-name.md when one exists. -->

Depends on: <!-- Link the prerequisite PR, or write N/A. For stacked PRs, state
the current base and retarget to main after the prerequisite merges. -->

## Changes

<!-- Describe the resulting behavior and the main implementation choices. -->

## Testing

<!-- List checks run and their outcomes, including coverage. Explain any limitations. -->

- [ ] Backend: ruff, mypy, pytest with coverage (at least 80%)
- [ ] Frontend: lint, typecheck, Vitest coverage, build, browser tests

## Quality & security

- [ ] Task issue linked, with acceptance criteria and current validation status
- [ ] Dependency audits pass; no failing gates bypassed or weakened
- [ ] No secrets, generated coverage, builds, or dependencies included
- [ ] Normal tests are deterministic and do not require real LLM credentials
- [ ] CodeQL reviewed when available; Sonar runs on main after merge

## Screenshots

<!-- For visible UI changes, include before/after screenshots where possible; otherwise N/A. -->

## Architectural notes

<!-- Explain tradeoffs, dependency changes, and any impact on SPEC.md. Use N/A when appropriate. -->

## Follow-up

<!-- Identify remaining work or operational setup, with issue links where available. -->
