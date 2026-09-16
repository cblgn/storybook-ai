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
├── TASKS/
│   └── 001-bootstrap.md
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
2. the relevant file under `TASKS/`;
3. `SPEC.md`;
4. `AGENTS.md`;
5. existing code and tests.

`SPEC.md` describes what the product should do.

`AGENTS.md` describes how the project should be developed.

Files under `TASKS/` describe individual implementation missions.

If a task conflicts with `SPEC.md`, identify the conflict before implementing it.

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
uv run ruff check .
uv run mypy src
```

---

# Frontend quality checks

Before frontend work is considered complete:

```bash
pnpm lint
pnpm build
pnpm test:e2e
```

---

# Development workflow

For every task:

1. Read the relevant task file if one exists.
2. Read the relevant sections of `SPEC.md`.
3. Inspect existing code.
4. Run `git status`.
5. Identify the smallest coherent implementation.
6. Add or update tests where appropriate.
7. Implement the change.
8. Run relevant quality checks.
9. Review the resulting Git diff.
10. Report what changed and any remaining limitations.

Do not rewrite unrelated code.

---

# Task files

Implementation missions may be stored under:

```text
TASKS/
```

Example:

```text
TASKS/
├── 001-bootstrap.md
├── 002-story-generation.md
└── 003-ui-polish.md
```

Task files are part of the repository history.

Once a task has been implemented, do not silently modify it to match the implementation.

If requirements change, create a new task or explicitly update the specification.

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

* it satisfies the relevant task and `SPEC.md`;
* code remains understandable;
* relevant tests pass;
* backend type/lint checks pass;
* frontend build succeeds when affected;
* the end-to-end workflow remains functional;
* the Git diff contains no unrelated modifications;
* no credentials or generated junk are committed.
