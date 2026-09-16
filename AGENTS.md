# Storybook AI — Agent Instructions

## Project purpose

Storybook AI is a small web application that generates personalized children's stories using an LLM.

The project has two goals:

1. build a usable AI-native web application;
2. experiment with agentic software development using Codex.

The project must remain small enough to understand and complete as a one-day MVP.

---

# Repository

This project is maintained as a single Git repository.

The repository contains both backend and frontend code.

Expected structure:

```text
storybook-ai/
├── .gitignore
├── AGENTS.md
├── SPEC.md
├── README.md
├── CONTRIBUTING.md
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── pull_request_template.md
│   └── workflows/
├── docs/
│   └── adr/
│
├── backend/
│   ├── pyproject.toml
│   ├── src/
│   └── tests/
│
└── frontend/
    ├── package.json
    ├── vite.config.ts
    └── src/
```

Do not create separate Git repositories for the frontend and backend.

---

# Source of truth

Before implementing a change, use these sources in this order:

1. the current user request;
2. the relevant GitHub Issue, when one exists;
3. `SPEC.md`;
4. `AGENTS.md`;
5. `CONTRIBUTING.md`;
6. existing code and tests.

`SPEC.md` is the versioned product specification: it defines product behavior and
requirements.

`AGENTS.md` defines stable development instructions for coding agents.

GitHub Issues define individual units of work: implementation tasks, bugs, and
enhancements. When an Issue exists, it is the authoritative task description.
Pull Requests represent their implementation; normally one implementation Issue
maps to one Pull Request.

`README.md` introduces the project and explains local setup. `CONTRIBUTING.md`
documents the human/GitHub contribution workflow. ADRs under `docs/adr/` record
only significant architectural decisions, not ordinary tasks or progress reports.

If an Issue conflicts with `SPEC.md`, identify the conflict before implementing it.
Update the specification explicitly when an authorized change alters product
requirements; do not silently treat an Issue as an amendment to the specification.

---

# Technology stack

## Backend

* Python 3.14+
* uv
* FastAPI
* Pydantic v2
* PydanticAI
* pytest
* ruff
* mypy

## Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* shadcn/ui
* pnpm

Do not introduce an additional backend, frontend, or agent framework without an explicit requirement.

---

# Development environment

Everything must run locally.

During development:

```text
React / Vite     http://localhost:5173
FastAPI          http://localhost:8000
```

The Vite frontend should proxy `/api` to FastAPI when practical.

No cloud infrastructure is required.

---

# Architecture

Use the following dependency direction:

```text
Browser
   ↓
React / TypeScript
   ↓
HTTP API
   ↓
FastAPI
   ↓
Application services
   ↓
PydanticAI agents
   ↓
LLM provider
```

Business logic must not live in FastAPI route handlers.

AI orchestration must not live in React components.

PydanticAI agents must not depend on HTTP concepts.

---

# Backend structure

Prefer:

```text
backend/
├── pyproject.toml
├── src/
│   └── storybook/
│       ├── api/
│       │   ├── app.py
│       │   └── routes/
│       │       └── stories.py
│       │
│       ├── domain/
│       │   ├── requests.py
│       │   └── stories.py
│       │
│       ├── agents/
│       │   ├── planner.py
│       │   ├── writer.py
│       │   └── reviewer.py
│       │
│       ├── services/
│       │   └── story_generator.py
│       │
│       └── settings.py
│
└── tests/
```

Avoid unnecessary layering.

Do not introduce repositories, CQRS, event buses, plugin systems, or database abstractions for the MVP.

---

# Frontend structure

Prefer:

```text
frontend/
├── package.json
├── vite.config.ts
└── src/
    ├── components/
    │   └── ui/
    │
    ├── features/
    │   └── story/
    │       ├── components/
    │       ├── api.ts
    │       └── types.ts
    │
    ├── lib/
    │   └── api.ts
    │
    ├── App.tsx
    └── main.tsx
```

Prefer feature-oriented organization.

Use shadcn/ui primitives when suitable.

Do not introduce global state management unless local React state becomes insufficient.

Do not introduce Redux for the MVP.

---

# Domain models

Use explicit Pydantic models.

Core concepts include:

```text
StoryRequest
StoryPlan
Character
StoryScene
StoryBook
StoryReview
```

Prefer structured LLM outputs over parsing arbitrary text.

The contract between the AI layer and the application should be typed.

---

# AI workflow

The target workflow is:

```text
StoryRequest
     ↓
Planner
     ↓
StoryPlan
     ↓
Writer
     ↓
StoryBook
     ↓
Reviewer
     ↓
StoryReview
```

If revision is necessary:

```text
StoryBook + StoryReview
          ↓
        Writer
          ↓
 revised StoryBook
```

Automatic revision is limited to one iteration.

Do not build uncontrolled agent loops.

---

# PydanticAI

Use PydanticAI as the application-level LLM framework.

Agents should have:

* one clear responsibility;
* focused instructions;
* typed outputs;
* explicit dependencies when necessary.

Do not introduce:

* LangChain;
* LangGraph;
* CrewAI;
* another agent orchestration framework.

The LLM provider must be configurable.

Prefer a Codex-compatible PydanticAI provider for local development when available.

Never hardcode credentials.

Never commit local authentication information.

---

# Planner

The planner converts the request into a structured story plan.

It may determine:

* story title;
* characters;
* setting;
* premise;
* challenge;
* important events;
* resolution;
* emotional or educational theme.

It must not write the complete story.

---

# Writer

The writer receives the request and story plan.

It generates a complete structured `StoryBook`.

The result must:

* suit the requested age;
* approximately match the requested duration;
* preserve character consistency;
* have a beginning, development, and ending;
* respect the requested hero, setting, and theme;
* avoid unnecessarily frightening content;
* finish positively or reassuringly.

---

# Reviewer

The reviewer evaluates the generated story.

It checks:

* age appropriateness;
* narrative coherence;
* character consistency;
* requested theme;
* approximate duration;
* frightening or disturbing content;
* quality of the ending.

It returns a structured `StoryReview`.

It must not rewrite the story itself.

---

# FastAPI

Keep routes thin.

Typical route:

```python
@router.post("/stories", response_model=StoryBook)
async def create_story(
    request: StoryRequest,
    service: StoryGeneratorService = Depends(...),
) -> StoryBook:
    return await service.generate(request)
```

HTTP concerns remain at the API boundary.

Do not pass FastAPI objects into the application or AI layers.

---

# API

The MVP exposes:

```text
POST /api/stories
GET /api/health
```

Do not add CRUD APIs without a real requirement.

---

# Frontend

The frontend must be a real React application.

Main workflow:

```text
story form
   ↓
generation
   ↓
story result
```

The UI must explicitly handle:

* initial state;
* invalid form state;
* loading state;
* success state;
* error state.

Prefer native React mechanisms:

* `useState`;
* `useReducer` when useful;
* a small fetch wrapper.

---

# Styling

The application should feel:

* warm;
* playful;
* modern;
* polished;
* readable.

It should be suitable for parents and children without becoming visually cluttered.

Use:

* Tailwind CSS;
* shadcn/ui;
* responsive layouts;
* readable typography;
* generous spacing.

Animations are optional.

Visual polish must not block delivery of the end-to-end MVP.

---

# Persistence

Persistence is not required for the initial MVP.

If added, prefer local JSON storage.

Do not introduce:

* PostgreSQL;
* Redis;
* cloud storage;
* an ORM;

unless explicitly requested later.

---

# Security and credentials

Never commit:

* `.env`;
* API keys;
* access tokens;
* Codex credentials;
* authentication files;
* secrets.

Provide `.env.example` when configuration through environment variables is needed.

`.env.example` must contain placeholders only.

---

# Git workflow

This project uses Git from its creation.

## General rules

Before making significant modifications:

```bash
git status
```

Inspect existing modifications before editing files.

Do not overwrite unrelated user changes.

Do not revert unrelated changes.

---

## Branch

The initial development branch is:

```text
main
```

Implementation work must use a dedicated feature branch and reach `main` through a pull request.

Do not introduce a complex Git workflow.

---

## Commits

Commits should be:

* small enough to understand;
* logically coherent;
* buildable when practical.

Good examples:

```text
chore: bootstrap project structure
feat: add story domain models
feat: implement story writer agent
feat: expose story generation API
feat: add story creation form
feat: add planner and reviewer workflow
```

Avoid commits mixing unrelated refactoring and features.

---

## Agent commit behavior

Do not automatically commit changes unless explicitly requested.

When asked to commit:

1. inspect `git status`;
2. inspect the diff;
3. run relevant quality checks;
4. commit only relevant changes;
5. use a concise descriptive commit message.

Do not use:

```text
git add .
```

blindly when unrelated modifications exist.

Do not:

* force push;
* rewrite history;
* amend existing commits;
* delete branches;

unless explicitly requested.

---

# .gitignore

The repository must ignore at least:

```gitignore
# Python
__pycache__/
*.py[cod]
.venv/
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Secrets
.env
.env.*
!.env.example

# Frontend
frontend/node_modules/
frontend/dist/

# Application data
data/

# IDE
.idea/
.vscode/

# OS
.DS_Store
Thumbs.db
```

Generated files should not be committed unless they are intentionally part of the repository.

---

# Testing

Backend tests should cover:

* Pydantic model validation;
* story generation orchestration;
* planner/writer/reviewer interactions with mocked agents;
* API happy path;
* API validation errors.

Default unit tests must not invoke a real LLM.

Real-provider tests, if created, must be separated and explicitly invoked.

Frontend testing should remain pragmatic.

Prioritize:

* form behavior;
* API integration boundaries;
* result rendering;

only when useful.

Do not spend a large portion of the MVP building an extensive frontend test suite.

---

# Backend quality checks

Before backend work is considered complete:

```bash
uv run pytest
uv run pytest --cov=src/storybook --cov-report=term-missing --cov-report=xml
uv run ruff check .
uv run mypy src
```

---

# Frontend quality checks

Before frontend work is considered complete:

```bash
pnpm lint
pnpm typecheck
pnpm test:coverage
pnpm build
pnpm test:e2e
```

If frontend tests exist:

```bash
pnpm test
```

---

# Development workflow

Follow `CONTRIBUTING.md`. For every change:

1. Inspect `git status`, the current branch, history, and existing modifications.
2. Read the relevant GitHub Issue and sections of `SPEC.md`.
3. Inspect existing code and identify the smallest coherent implementation.
4. Start a dedicated branch from an up-to-date `main`, preserving unrelated work.
5. Implement the change and add or update meaningful tests where appropriate.
6. Run the relevant local quality checks and locked dependency audits.
7. Inspect `git status` again and review the complete diff before finishing,
   including new files, even when no commit or PR is requested.
8. Report the related Issue, changes, validation results, and remaining limitations.
9. When publication is authorized, create the linked PR and verify the required
   GitHub CI/security checks before proposing a merge.

Do not rewrite unrelated code.

---

# Temporary bootstrap migration

`TASKS/001-bootstrap.md` and `TASKS/002-github-quality.md` are legacy bootstrap
artifacts retained temporarily for GitHub migration. Preserve their contents until
both tasks are represented by GitHub Issues and their Pull Requests have merged.
Only then may a separate change remove `TASKS/`. Future work must originate in
GitHub Issues; do not create new task files. GitHub assigns Issue and PR numbers
from a shared sequence, so record the actual links rather than assuming numbers
match the legacy task identifiers.

---

# Simplicity rule

This is initially a one-day MVP.

Prefer:

```text
simple and complete
```

over:

```text
generic and unfinished
```

Avoid premature:

* factories;
* registries;
* dependency injection frameworks;
* event buses;
* plugin systems;
* microservices;
* background queues;
* elaborate DDD abstractions.

Separation of concerns matters.

Enterprise ceremony does not.

---

# Out of scope

Unless explicitly requested, do not implement:

* authentication;
* accounts;
* payments;
* AWS infrastructure;
* cloud deployment;
* Kubernetes;
* Redis;
* Celery;
* database persistence;
* image generation;
* audio generation;
* email;
* social sharing.

---

# Definition of done

A change is complete when:

* it satisfies the relevant Issue (or explicit user request) and `SPEC.md`;
* code remains understandable;
* relevant tests pass;
* backend type/lint checks pass;
* frontend build succeeds when affected;
* the end-to-end workflow remains functional;
* the Git diff contains no unrelated modifications;
* no credentials or generated junk are committed.

# GitHub development workflow

The repository uses pull requests and automated quality gates.

## Task and issue traceability

Write GitHub Issue titles and bodies in English, including requirements,
acceptance criteria, and technical notes. Agent-authored Issue updates must also
be in English, even when the user conversation or application UI is in French.
Preserve code identifiers and quoted UI text in their original language.

Future implementation work starts from a GitHub Issue. Search existing Issues
first and reuse the matching Issue; do not create duplicates. Respect explicit
user limits on remote operations. If remote work is not authorized or GitHub is
unavailable, continue authorized local work, prepare descriptions locally, and
report the pending Issue/PR linkage rather than claiming it already exists.

For each Issue:

1. Use its objective, requirements, scope, and acceptance criteria as the task
   description. Link relevant `SPEC.md` sections rather than copying the product
   specification into the Issue.
2. Record the Issue number in progress updates and keep implementation and
   validation status accurate.
3. Normally use one branch and one PR per implementation Issue. Include
   `Closes #<issue>` in the PR description, with the reason for the change, its
   scope, checks and results, limitations, and screenshots for UI changes.
   Link the PR from the Issue as well. Explain any exception to the one-to-one
   mapping in the Issue and PR.
4. Prefer independent PRs targeting `main`. If a dependent PR must temporarily
   target another feature branch, state that dependency explicitly. After the
   prerequisite is squash merged, reconcile the dependent branch with `main`
   without rewriting published history, retarget its PR, review the complete
   diff, and rerun checks. Do not merge a dependent PR into the prerequisite
   feature branch.
5. Leave the Issue open while the PR awaits merge. Closing keywords
   take effect when the PR targets and is merged into the default
   branch; do not report a task as delivered to `main` before that happens.

Issue tracking does not authorize automatic commits or merges. Follow the commit
and merge authorization rules below. Record a significant architectural decision
in an ADR only when needed; link it from the Issue and PR.

## Branches and pull requests

Direct feature development on `main` is not allowed.

For implementation work, use a dedicated branch with a meaningful name, for example:

```text
feat/12-story-writer
fix/18-story-duration
ci/23-codeql
docs/27-architecture
```

Use Conventional Commit-style commit messages:

```text
feat: add story writer agent
fix: prevent duplicate story generation
test: cover reviewer revision workflow
ci: add dependency security checks
chore: update dependencies
docs: document local setup
```

Before proposing a pull request:

1. inspect `git status`;
2. review the complete diff;
3. run all relevant backend checks;
4. run all relevant frontend checks;
5. ensure no credentials or generated files are included;
6. verify the application still builds;
7. summarize both the reason for the change and the implementation.

A pull request description must explain **why** the change exists, not merely repeat the Git diff.

For visible frontend changes, include a screenshot in the pull request when possible.

Do not merge a pull request without explicit user authorization.

When a merge is authorized, use squash merge into `main` after the required checks
and review pass. The squash commit message must follow Conventional Commits.
Use GitHub's automatic deletion of merged head branches when configured; do not
manually delete branches without authorization. Document repository settings in
`CONTRIBUTING.md`; documentation alone does not configure GitHub.

Do not push directly to `main`.

Do not bypass failing GitHub checks.

Do not weaken tests, linting, type checking, coverage requirements, security checks, branch protections, or quality gates merely to make a change pass.

If a quality check exposes a legitimate defect, fix the defect.

If a check itself is incorrect or inappropriate, explain why before changing its configuration.

Do not automatically commit unless the task explicitly asks for commits.

When commits are explicitly requested:

* keep commits logically coherent;
* do not include unrelated files;
* use clear Conventional Commit messages;
* never rewrite published history unless explicitly requested.

Dependency updates should normally be handled through Dependabot pull requests.

Automated tests must not call a real LLM unless they are explicitly marked as integration tests.

Normal CI must remain deterministic and must not require Codex, OpenAI, or other LLM credentials.

Backend coverage must remain at least 80%. Keep the default exclusion of real-provider
`integration` tests and the test guards that prohibit real model requests.

Run the locked dependency audits described in `CONTRIBUTING.md`. High and critical
vulnerabilities must fail CI; the backend audit fails on all known vulnerabilities.

Inspect Git status and the complete task diff before finishing any implementation,
even when no commit or pull request is requested.
