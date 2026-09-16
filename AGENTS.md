# Storybook AI — Agent Instructions

## Purpose

Storybook AI is a local-first web application that generates personalized children's stories using an LLM.

The project is also used to practice high-quality agentic software development with Codex.

Prefer simple, explicit, production-quality solutions over speculative architecture.
Keep the one-day MVP proportionate, backend and frontend in one repository, and
the application runnable locally without unnecessary cloud infrastructure.

## Sources of truth

Use these sources in this order:

1. the current authorized user request;
2. the relevant GitHub Issue, when one exists;
3. `SPEC.md` for expected product behavior;
4. `AGENTS.md` for permanent agent rules;
5. `CONTRIBUTING.md` for the human Git/GitHub workflow;
6. existing code and tests.

A PR is the implementation and review of an Issue. [ADRs](docs/adr/README.md)
record significant architectural rationale; [SECURITY.md](SECURITY.md) owns
private vulnerability reporting. Use [README.md](README.md) for local setup.
Do not create local Markdown task files.

If an Issue conflicts with `SPEC.md`, identify the conflict before implementation. Update `SPEC.md` only when an authorized change modifies expected product behavior.

## Instruction precedence

Explicit user instructions take precedence over workflow guidance in skills.

Skills provide the default repository workflow, but they must not override
an explicit authorized user request.

If a skill conflicts with another repository instruction, follow the
source-of-truth order defined above and report the conflict.

## Stack

### Backend

- Python 3.14+
- uv
- FastAPI
- Pydantic v2
- PydanticAI
- pytest
- ruff
- mypy

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- pnpm

Do not introduce another backend, frontend, or agent framework without an explicit requirement. Read manifests and lockfiles for exact versions.

## Architecture invariants

- React owns presentation and browser interaction.
- FastAPI is the HTTP boundary.
- Application services orchestrate use cases without depending on HTTP objects.
- PydanticAI agents handle semantic generation, interpretation, or review.
- Business logic must not live in FastAPI route handlers.
- AI orchestration must not live in React components.
- PydanticAI agents must not depend on HTTP concepts.
- Prefer typed structured outputs over parsing free-form LLM text.
- Prefer deterministic Python for deterministic behavior.
- Keep dependencies explicit.
- Prefer feature-oriented React code, native state and existing shadcn/ui primitives;
  do not introduce Redux for the MVP.
- Avoid speculative abstractions, unnecessary layers, and infrastructure without a current requirement.

## AI and PydanticAI invariants

- PydanticAI is the application LLM framework.
- Agents must have focused responsibilities.
- LLM providers must remain configurable.
- Prefer the existing Codex-compatible PydanticAI provider for local development
  when available.
- Prompts must not become hidden application logic when deterministic code is more appropriate.
- Revision/retry loops must be bounded.
- Do not introduce LangChain, LangGraph, CrewAI, or another orchestration framework unless explicitly required.
- Never hardcode or commit provider credentials.

## Testing and quality

Normal automated tests must be deterministic and must not call a real LLM.

Normal CI must not require LLM credentials; preserve guards against real model
requests. Real-provider tests remain opt-in, marked `integration`, and excluded
from the default suite and required PR checks.

Backend checks when affected, starting from the repository root:

```bash
cd backend
uv run ruff check .
uv run mypy src
uv run pytest --cov=src/storybook --cov-report=term-missing
```

Frontend checks when affected, starting from the repository root:

```bash
cd frontend
pnpm lint
pnpm typecheck
pnpm test:coverage
pnpm build
```

Run end-to-end tests when the affected workflow requires them.

Backend coverage must remain at least 80%. Do not add meaningless tests or invent
an arbitrary frontend coverage threshold. Use the locked audits in
[CONTRIBUTING.md](CONTRIBUTING.md#vérifications-locales): backend fails on all known
vulnerabilities, frontend on high/critical findings. Preserve `uv --no-build` and
pnpm’s explicit dependency build-script allowlist.
For documentation-only changes, validate references, skill metadata and the full
diff; explain inapplicable application checks. Required remote checks still apply.

Do not weaken tests, type checking, linting, coverage, security checks, Sonar rules, or repository protections merely to make a change pass.
If a check itself is incorrect, explain the evidence before changing it.

## Git and GitHub invariants

- Inspect `git status`, the branch and existing changes before significant work.
- Non-trivial implementation work must be represented by a GitHub Issue.
- Include the Issue number in the branch name. Write Issue titles, bodies and
  updates in English, preserving quoted UI text and code identifiers.
- Commit and publish only within existing user authorization; reuse it across skills.
- Do not develop features directly on `main`.
- Use one Issue and one Pull Request by default for one independently deliverable change.
- Use Conventional Commits.
- Do not force-push, rewrite published history, amend commits or manually delete
  branches unless explicitly authorized.
- Do not push directly to `main`.
- Do not merge or enable auto-merge without explicit authorization for that PR.
  Authorized merges use squash after required checks and review; Dependabot’s
  approved automation does not authorize an agent to merge other PRs.
- Do not bypass required GitHub checks or branch protections.
- Do not overwrite or revert unrelated user changes.
- Inspect `git status` and the full diff, including new files, before committing
  and finishing. Stage only relevant files; keep the Issue open until merge.

## Security invariants

- Never commit secrets, tokens, local authentication files, or populated `.env` files.
- Never expose secret values in logs, Issues, PRs, or prompts.
- Fix legitimate security findings rather than suppressing them without justification.
- Respect the repository's GitHub Actions pinning and least-privilege policy.
- Dependabot is the preferred mechanism for routine dependency updates.
- Keep `.env.example` placeholder-only; [.gitignore](.gitignore) owns exclusion
  rules. Only intended skill files belong in tracked `.codex` paths.
- New Actions require justification and verified full-SHA pins from approved vendors.
- The [security baseline](docs/repository-security.md) is intentional. Never
  disable controls or add protection bypasses; unreadable protection fails closed.
- Report sensitive findings privately through `SECURITY.md`.

## Skills

Use [refine-work-item](.codex/skills/refine-work-item/SKILL.md) when a non-trivial informal request is not yet represented by a suitable GitHub Issue.

Use [implement-issue](.codex/skills/implement-issue/SKILL.md) to implement an existing GitHub Issue.

Use [prepare-pull-request](.codex/skills/prepare-pull-request/SKILL.md) after implementation to publish and validate the change as a Pull Request.

Use [senior-architecture-review](.codex/skills/senior-architecture-review/SKILL.md) when a change introduces or materially changes an architectural boundary, abstraction, persistence model, external dependency, agent workflow, concurrency model, security boundary, or significant cross-cutting concern.

Use [harden-repository](.codex/skills/harden-repository/SKILL.md) for GitHub repository settings, Actions security, rulesets, CodeQL, Dependabot, Sonar, secret protection, or repository hardening.

Architecture review is not required for trivial or purely mechanical changes.
Load only relevant skills. When the request authorizes the complete workflow,
continue through refinement → implementation → PR preparation without artificial
stops between skills. A skill does not grant additional authorization.

## Default feature flow

For a normal non-trivial product change, the default workflow is:

1. `refine-work-item` when no suitable Issue exists;
2. `senior-architecture-review` when the change meets its trigger conditions;
3. `implement-issue`;
4. `senior-architecture-review` again on the final diff when the architectural impact is significant;
5. `prepare-pull-request` when publication is requested.

Do not force every skill into every change.
Use only the skills relevant to the task.

## Simplicity

Prefer the simplest complete solution that satisfies current requirements.

Do not design for hypothetical future requirements.

Add an abstraction only when it makes an existing boundary or variation clearer.

## Definition of done

A change is done when:

- the authorized requirement and acceptance criteria are satisfied;
- relevant tests and quality checks pass;
- the implementation remains understandable;
- the complete diff contains no unrelated changes;
- no secrets or generated junk are included;
- product documentation is updated when expected behavior changed;
- the Pull Request is ready for maintainer review when publication was requested.
