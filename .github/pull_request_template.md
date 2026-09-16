## Summary

<!-- Describe the resulting behavior in one or two sentences. -->

Closes #<!-- Required: existing GitHub task issue number. -->

Depends on: <!-- Link prerequisite Issues/PRs, or write N/A. Normally target main;
explain any temporary dependency branch and the plan to retarget after squash merge. -->

## Why

<!-- What problem does this solve, for whom, and why now? Link the relevant
SPEC.md sections without duplicating them. Explain any authorized requirement change. -->

## Changes

<!-- Describe the resulting behavior and the main implementation choices. -->

## Testing

<!-- List relevant commands and outcomes, including coverage. Explain skipped or
inapplicable checks and limitations; do not claim checks that were not run. -->

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

<!-- Explain tradeoffs, dependency changes, and any impact on SPEC.md. Link an ADR
under docs/adr/ only for a significant architectural decision; otherwise use N/A. -->

## Follow-up

<!-- Link follow-up GitHub Issues and remaining operational setup. Do not create
task files. Record any dependency that must be resolved before squash merge. -->
