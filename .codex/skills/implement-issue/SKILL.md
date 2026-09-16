---
name: implement-issue
description: Implement an existing GitHub Issue as a locally validated change on its dedicated branch. Use for features, bugs, refactorings, significant documentation and normal CI improvements.
---

# Implement Issue

## Purpose

Implement an existing GitHub Issue as a tested local change on a dedicated branch.

This skill focuses on implementation. Publishing the final Pull Request belongs to [prepare-pull-request](../prepare-pull-request/SKILL.md).

## Preconditions

- A GitHub Issue exists and is the work-item source of truth.
- The repository is available locally.

## Workflow

1. Read [AGENTS.md](../../../AGENTS.md).
2. Read the Issue and relevant sections of [SPEC.md](../../../SPEC.md).
3. Read [CONTRIBUTING.md](../../../CONTRIBUTING.md) when Git workflow details are needed.
4. Inspect `git status`, current branch, and existing modifications.
5. For new work, update local `main` from `origin/main` with a fast-forward,
   preserving local work. For a continuation, reuse the existing Issue branch/PR;
   do not restart it or discard its changes.
6. For new work, create a dedicated branch containing the Issue number, for example:
   - `feat/42-recurring-characters`
   - `fix/51-story-duration`
   - `refactor/63-agent-boundary`
7. Inspect the relevant code and tests before editing.
8. Determine the smallest implementation satisfying the acceptance criteria.
9. Use [senior-architecture-review](../senior-architecture-review/SKILL.md) first when the change meets its trigger conditions.
10. Implement the Issue end-to-end.
11. Add or update meaningful tests when changed behavior warrants them; do not
    add application tests for documentation-only changes.
12. Update [SPEC.md](../../../SPEC.md) if expected product behavior changes.
13. Add an ADR only for a significant long-term architectural decision.
14. Run relevant checks from [CONTRIBUTING.md](../../../CONTRIBUTING.md#vérifications-locales),
    preserving the invariants in [AGENTS.md](../../../AGENTS.md).
15. Review every acceptance criterion.
16. Inspect `git status` and the complete diff, including untracked files.

## Implementation rules

- Do not modify unrelated functionality.
- Prefer the simplest coherent solution.
- Do not add speculative abstractions or infrastructure.
- Deterministic behavior belongs in normal code, not prompts.
- Normal tests must not call real LLMs.
- Do not weaken quality or security checks to make the implementation pass.
- Preserve unrelated user modifications.

## Architecture checkpoint

For a significant architectural change, run [senior-architecture-review](../senior-architecture-review/SKILL.md) again on the actual diff before considering implementation complete.

## Completion

Produce a focused, locally validated implementation. Preserve unrelated local
files; "clean" does not mean deleting the user’s work. When publication is already
authorized, continue with [prepare-pull-request](../prepare-pull-request/SKILL.md).
Otherwise stop at the requested local deliverable.

Report:

- Issue number;
- branch name;
- files/areas changed;
- acceptance criteria status;
- checks executed and results;
- architecture review findings when applicable;
- remaining concerns.

Do not merge anything.
