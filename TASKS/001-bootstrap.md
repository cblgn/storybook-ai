# Task 001 — Bootstrap Storybook AI

## Objective

Bootstrap the Storybook AI repository and establish the shortest path toward a working end-to-end MVP.

Read:

```text
AGENTS.md
SPEC.md
```

before making any implementation decisions.

---

# Phase 1 — Analysis

Before writing code:

1. inspect the repository;
2. inspect Git status;
3. read `AGENTS.md`;
4. read `SPEC.md`;
5. identify the smallest architecture capable of satisfying the MVP;
6. produce a concise implementation plan.

Do not introduce infrastructure or abstractions that are not required by the specification.

The project should remain achievable in one day.

---

# Phase 2 — Repository bootstrap

If the directory is not already a Git repository:

```bash
git init
git branch -M main
```

Create the basic repository structure:

```text
storybook-ai/
├── .gitignore
├── AGENTS.md
├── SPEC.md
├── README.md
├── TASKS/
│   └── 001-bootstrap.md
├── backend/
└── frontend/
```

Do not create commits unless explicitly requested.

---

# Phase 3 — Backend bootstrap

Create a Python project under:

```text
backend/
```

using:

* Python 3.13+;
* uv;
* FastAPI;
* Pydantic v2;
* PydanticAI;
* pytest;
* ruff;
* mypy.

Create the smallest package structure needed for the application.

Provide:

```text
GET /api/health
```

returning a simple healthy response.

Do not implement the complete AI workflow yet unless necessary to validate the architecture.

---

# Phase 4 — Frontend bootstrap

Create a frontend under:

```text
frontend/
```

using:

* React;
* TypeScript;
* Vite;
* Tailwind CSS;
* shadcn/ui;
* pnpm.

Create a minimal Storybook AI page.

Configure frontend development so that `/api` can reach the FastAPI backend.

Verify that the frontend can successfully call:

```text
GET /api/health
```

---

# Phase 5 — Vertical slice

After both projects are initialized, implement the smallest possible end-to-end story generation vertical slice.

The initial slice may temporarily use only the Writer agent.

Target flow:

```text
React form
   ↓
POST /api/stories
   ↓
FastAPI
   ↓
StoryGeneratorService
   ↓
PydanticAI Writer
   ↓
StoryBook
   ↓
React rendering
```

Use structured Pydantic output.

Do not implement Planner or Reviewer before this vertical slice works.

---

# Phase 6 — Validation

Backend:

```bash
uv run pytest
uv run ruff check .
uv run mypy src
```

Frontend:

```bash
pnpm lint
pnpm build
```

Also verify manually that:

1. the React application loads;
2. the frontend can reach FastAPI;
3. a valid story request can reach the backend;
4. a generated story is returned;
5. React displays the result.

---

# Constraints

Do not introduce:

* database persistence;
* authentication;
* Docker unless needed;
* AWS;
* Redis;
* Celery;
* Next.js;
* Redux;
* LangChain;
* LangGraph;
* CrewAI;
* unnecessary architectural abstractions.

Do not add Planner or Reviewer until the basic Writer vertical slice works.

Do not commit credentials.

Do not commit `.env`.

Do not make Git commits unless explicitly requested.

---

# Expected outcome

At the end of this task, the repository should contain:

* a valid Git repository;
* a working FastAPI project;
* a working React/Vite project;
* backend and frontend quality tooling;
* a health-check connection between frontend and backend;
* preferably the first working story-generation vertical slice.

If the complete vertical slice cannot be achieved cleanly during bootstrap, leave the repository in a passing, runnable state and clearly identify the next smallest implementation step.

