# Storybook AI — Agent instructions

## Project

Storybook AI generates personalized children's stories with an LLM. It is both a
usable web application and an experiment in agent-assisted development.

Keep the project small enough to understand and complete as a one-day MVP.
Prefer simple, complete changes over speculative abstractions or infrastructure.
Everything must work locally; cloud services and paid infrastructure are not
required for the application. Keep backend and frontend in this one repository.

Use [README.md](README.md) for setup and [SPEC.md](SPEC.md) for product scope.
Do not expand that scope merely because a framework or service is available.

## Sources of truth

Use these sources in order:

1. The current authorized user request.
2. The relevant GitHub Issue, when one exists.
3. [SPEC.md](SPEC.md).
4. This `AGENTS.md`.
5. [CONTRIBUTING.md](CONTRIBUTING.md).
6. Existing code and tests.

Each source has a distinct responsibility:

- A GitHub Issue is the authoritative description of the current work item.
- `SPEC.md` defines expected product behavior and functional requirements.
- `AGENTS.md` defines permanent coding-agent rules and architectural invariants.
- `CONTRIBUTING.md` describes the human contribution workflow and local commands.
- A Pull Request contains the implementation and its review.
- [ADRs](docs/adr/README.md) record significant architectural rationale only.
- [SECURITY.md](SECURITY.md) defines private vulnerability reporting.

Identify conflicts with the specification before implementation. An authorized
product change must explicitly update the specification; do not silently treat
an Issue or an existing implementation as a replacement specification.

Use GitHub Issues for work tracking; do not create Markdown task files.

## Technology stack

- Backend: Python 3.14+, uv, FastAPI, Pydantic v2 and PydanticAI.
- Backend quality: pytest, pytest-cov, Ruff and mypy.
- Frontend: React, TypeScript, Vite, Tailwind CSS, shadcn/ui and pnpm.
- Frontend quality: ESLint, TypeScript, Vitest/Testing Library and Playwright.

Read the manifests and lockfiles for exact versions. Do not introduce another
backend, frontend or agent framework without an explicit requirement.
Use lockfiles and preserve dependency build restrictions: uv's `--no-build`
and pnpm's explicit build-script allowlist.

## Architecture invariants

Preserve this dependency direction:

```text
React → HTTP API → FastAPI → application services → PydanticAI agents → provider
```

React owns presentation and interaction state, not AI orchestration.
FastAPI owns HTTP concerns, not business logic. Keep route handlers thin.
Application services orchestrate use cases without depending on HTTP objects.
PydanticAI agents must remain independent of FastAPI and HTTP concepts.
Use explicit Pydantic models and typed structured outputs at AI boundaries.

Prefer feature-oriented frontend organization and existing shadcn/ui primitives.
Use native React state and a small fetch boundary; add broader state management
only when local state is demonstrably insufficient. Do not introduce Redux for
the MVP.

Keep layering proportionate to the problem. Do not add speculative repositories,
CQRS, event buses, registries, dependency-injection frameworks, microservices,
background queues, plugin systems or database abstractions.
Storage and infrastructure choices must follow the scope in `SPEC.md`.

## PydanticAI and LLM invariants

PydanticAI is the application's LLM framework. Do not add LangChain, LangGraph,
CrewAI or another orchestration framework without an explicit requirement.

Give each agent a focused responsibility, clear instructions and typed outputs.
Prefer structured results over parsing arbitrary generated text. Declare
explicit dependencies when needed; keep provider selection configurable.
Prefer the existing Codex-compatible PydanticAI provider for local development
when available. Never hardcode or copy credentials into the repository.

Planner, Writer, Reviewer, story models and revision behavior are specified in
`SPEC.md`; do not redefine them here or build uncontrolled agent loops.

Normal tests and CI must be deterministic and must not call a real LLM or require
Codex, OpenAI or other provider credentials. Keep the test guards prohibiting real
model requests. Use mocks or PydanticAI test models at the appropriate boundary.
Real-provider tests remain explicitly opt-in, marked `integration`, and excluded
from the default suite and required PR validation.

## Testing and quality invariants

Run the relevant checks for the affected components. The exact local commands
and locked dependency audits live in [CONTRIBUTING.md](CONTRIBUTING.md#vérifications-locales).

- Backend: Ruff, mypy, pytest and coverage; coverage must remain at least **80%**.
- Frontend: ESLint, TypeScript checking, Vitest coverage, production build and
  browser integration tests when affected.
- Dependencies: audit the locked runtime and development dependencies. The
  backend audit fails on all known vulnerabilities; frontend high/critical
  findings fail its audit.

Tests should check behavior and useful failure boundaries: model validation,
service orchestration, API success/errors, form behavior and story rendering.
Avoid meaningless tests added only to improve a coverage number. Keep frontend
testing proportionate to the MVP; do not invent an arbitrary coverage threshold.

Never weaken tests, linting, typing, coverage, security checks or Quality Gates
merely to obtain a passing build. Fix legitimate defects. If a check itself is
incorrect, explain the evidence before proposing its correction.

For documentation-only changes, validate links, skill metadata and the complete
diff; state which application checks are not relevant. Required remote checks
still apply to the PR.

## Git and GitHub invariants

Inspect `git status`, the branch and existing modifications before significant
work. Preserve unrelated user changes; do not overwrite or revert them.

Non-trivial work uses a GitHub Issue and a dedicated branch with its Issue number.
Normally one implementation Issue maps to one PR. Write Issue titles, bodies and
updates in English. Keep code identifiers and quoted UI text in their language.

Do not develop features or push directly on `main`. Use Conventional Commits.
Commit and publish only when the user's task authorizes those actions; respect
any explicit limits on remote operations and reuse authorization already given.

Never merge a PR without explicit user authorization. Authorized merges use
squash after required checks and review. The existing Dependabot automation is a
separate approved policy; it does not authorize an agent to merge other PRs.

Do not force-push, rewrite published history, amend commits or manually delete
branches without authorization. Preserve the intentional branch/ruleset
protections; never add bypasses or remove required checks to unblock a merge.

Inspect `git status` and the complete task diff, including new files, before
committing and before finishing. Stage only relevant files. Do not claim a PR is
merged or an Issue delivered while it is still awaiting review.

## Security invariants

Never commit or expose secrets, API keys, tokens, local authentication files or
real `.env` contents. Keep `.env.example` values as placeholders only.
The actual [.gitignore](.gitignore) is authoritative for ignored files; keep
credentials, caches, generated builds, coverage and local application data out of
Git. Only intentional repository skill files belong under the tracked `.codex` paths.

Security controls are intentional. Never disable features, weaken protection or
suppress findings to make checks pass. Fix findings or document a justified review.
Use `SECURITY.md` for sensitive reports; do not publish exploit details or secrets.

Respect the repository's verified full-SHA Action pinning and approved-vendor
policy. New Actions need a concrete justification and least-privilege permissions.
Normal dependency updates should use Dependabot.

The maintained security baseline is [docs/repository-security.md](docs/repository-security.md).
A successful configuration write is not proof of effective protection. Missing
or unreadable protection state must fail closed.

## Skills

For non-trivial feature, bug-fix, refactoring, significant documentation, normal
CI/CD or implementation work, read and use
[implement-github-issue](.codex/skills/implement-github-issue/SKILL.md).

For repository security, GitHub configuration, Sonar, Actions security, rulesets
or repository hardening work, also read and use
[harden-repository](.codex/skills/harden-repository/SKILL.md).
Do not load the hardening procedure for every normal feature.

These are repository-local skill entrypoints. Follow their links when the task
matches; load detailed procedures only when relevant. Skills do not grant extra
permissions or override the current authorized request.

## Definition of done

- The authorized work item and applicable specification are satisfied.
- The change remains understandable and contains no unrelated modifications.
- Relevant local checks and required PR checks pass; limitations are explicit.
- The full diff contains no secrets, generated junk or weakened protections.
- Documentation and the Issue/PR accurately describe the outcome and validation.
- A PR awaiting maintainer review remains unmerged until explicitly authorized.
