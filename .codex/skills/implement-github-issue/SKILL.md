---
name: implement-github-issue
description: Implement a scoped GitHub Issue through a validated Pull Request in Storybook AI. Use for features, bugs, refactorings, significant documentation changes and normal CI/CD improvements.
---

# Implement a GitHub Issue

Deliver one reviewable work item, with evidence for its acceptance criteria and a
PR ready for maintainer review. This skill describes the agent procedure; it does
not authorize commits, remote changes or merges beyond the user's request.
Reuse authorization already given and respect explicit restrictions on publishing.

All repository paths and commands below are relative to the repository root.

## Establish the work item

1. Inspect `git status`, the current branch, recent history and existing changes.
   Preserve unrelated work. Read [AGENTS.md](../../../AGENTS.md), relevant parts of
   [SPEC.md](../../../SPEC.md), and [CONTRIBUTING.md](../../../CONTRIBUTING.md).
   Inspect the implementation and tests before choosing an approach.
2. Search existing open and closed GitHub Issues for the request. Reuse an
   appropriate existing Issue rather than create a duplicate. A related closed
   Issue is context, not proof that a new scope is already tracked.
3. Refine the request into a small deliverable. Split oversized work into separate
   Issues before implementation, with explicit dependencies. Normally one Issue
   maps to one branch and one PR; explain exceptions in the Issue and PR.
4. If needed and authorized, create the Issue in English using the relevant
   [issue template](../../../.github/ISSUE_TEMPLATE/feature.md), including:
   **Context**, **Objective**, **Requirements**, **Acceptance criteria**,
   **Technical notes**, and **Out of scope**. For bugs, also include a reproducible
   failure and expected/actual behavior from the
   [bug template](../../../.github/ISSUE_TEMPLATE/bug.md).
   Link specification sections instead of copying the product specification.
5. Record the Issue number and keep scope and validation status accurate. English
   also applies to agent-authored Issue updates; preserve quoted UI text and code
   identifiers in their original language.

Non-trivial implementation needs an Issue unless the user explicitly exempts it.
A trivial typo or formatting correction may skip an Issue when tracking would add
more overhead than value. Never create local Markdown task files as a substitute.
If remote operations are prohibited or unavailable, prepare the Issue/PR text
locally, continue authorized independent work, and report the missing linkage.

## Prepare and implement

- Start from current `main`, updating with a fast-forward while preserving local
  changes. Create a dedicated branch with the Issue number; use the naming
  conventions in `CONTRIBUTING.md`, such as `feat/12-story-writer`.
- State a concise implementation plan: scope, affected boundaries, acceptance
  criteria and relevant validation. Identify specification conflicts before coding.
- Implement the smallest coherent solution. Update `SPEC.md` when an authorized
  change alters expected product behavior. Follow the architecture in `AGENTS.md`
  rather than restating it here.
- Add an [ADR](../../../docs/adr/README.md) only for a significant, long-term
  architectural decision. Routine tasks, progress and minor choices stay in the
  Issue/PR; do not create an ADR by default.
- Add or update meaningful tests for changed behavior and failure boundaries.
  Normal tests are deterministic, do not call real LLMs, and need no LLM credentials.
  Keep real-provider integration tests explicitly opt-in and outside normal CI.
- Use the [harden-repository skill](../harden-repository/SKILL.md) only when the task
  actually involves repository security/configuration, Sonar or hardening. Merely
  running existing CI does not require loading that procedure.

## Validate the change

Use the exact commands in
[CONTRIBUTING.md](../../../CONTRIBUTING.md#vérifications-locales) for affected areas:

- Backend: Ruff, mypy, pytest and coverage, preserving the 80% minimum.
- Frontend: lint, TypeScript checking, Vitest coverage, production build and
  relevant browser integration tests.
- Dependency or CI changes: applicable locked audits and workflow syntax checks.
- Documentation-only changes: references, skill metadata when relevant, obsolete
  instructions and the complete diff. Explain inapplicable application checks.

Do not modify thresholds or tests just to obtain green results. Investigate each
failure and fix its cause; explain evidence before correcting an erroneous check.
Do not generate meaningless tests to manipulate coverage or require real-provider
credentials for ordinary validation.

Before committing, inspect `git status` and the full work-item diff against its
base, including untracked/new files. Check that it contains no unrelated changes,
secrets, local authentication, generated reports, builds or installed dependencies.
Review lockfile changes when dependencies change. Stage named files deliberately;
never blindly stage all user modifications.

## Publish and review

When the user has authorized publication:

1. Create coherent Conventional Commits. Follow the human workflow's conventions;
   do not manufacture micro-commits or rewrite published history.
2. Push the Issue branch and open a PR targeting `main` with the
   [PR template](../../../.github/pull_request_template.md).
3. Include `Closes #<issue>`, the reason for the change, resulting behavior, scope,
   validation evidence, security considerations and limitations. Add screenshots
   for visible frontend changes when practical. GitHub's closing reference links
   the Issue and PR; verify that relationship without prematurely closing the Issue.
4. Monitor required GitHub checks after each push. Inspect failed logs, fix
   legitimate causes and repeat relevant validation. Never bypass protections,
   remove checks, weaken gates or suppress security findings to unblock the PR.
5. Review available CodeQL, dependency-security and Sonar results against the
   actual revision. Sonar currently runs on `main` after merge; do not claim the
   PR was analyzed if it was not. Record any unavailable result honestly rather
   than merging just to obtain one.
6. Inspect final status and the complete PR diff, including fixes added during CI.
   Report the Issue, branch, PR, checks and remaining limitations. Stop with the
   PR ready for maintainer review; leave its Issue open until merge.

Prefer independent PRs. For a necessary temporary dependency branch, document the
prerequisite, then reconcile with `main` after its squash merge without rewriting
published history. Retarget to `main`, review the resulting diff and rerun checks;
do not merge into an intermediate feature branch to bypass normal review.

**Never merge or enable PR auto-merge without explicit user authorization for it.**
The repository's approved Dependabot automation does not grant an agent permission
to merge unrelated PRs. Creating a PR or obtaining green checks is not merge approval.
