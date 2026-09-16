
# Task 002 — GitHub quality and security baseline

## Objective

Establish a professional GitHub development workflow for Storybook AI before further functional development.

The repository must use automated CI, security checks, dependency management, pull request standards, coverage reporting, and SonarQube Cloud analysis.

Read the following before modifying anything:

```text
AGENTS.md
SPEC.md
TASKS/001-bootstrap.md
```

Inspect the existing repository and preserve all working code.

---

## GitHub structure

Create or update:

```text
.github/
├── workflows/
│   ├── ci.yml
│   ├── security.yml
│   ├── codeql.yml
│   └── sonar.yml
├── dependabot.yml
└── pull_request_template.md
```

Also create:

```text
sonar-project.properties
```

---

## Backend CI

The backend CI must run:

```text
ruff
mypy
pytest
pytest-cov
```

The initial coverage threshold is:

```text
80%
```

Normal CI tests must never make a real LLM API call.

Use mocked agents, PydanticAI test models, or equivalent deterministic test doubles.

Ensure the project's development dependencies contain everything required by CI.

---

## Frontend CI

The frontend CI must run:

```text
eslint
TypeScript type checking
Vitest
coverage
production Vite build
```

If the frontend does not yet contain a minimal test setup, configure:

```text
Vitest
Testing Library
jsdom
@vitest/coverage-v8
```

Add appropriate package scripts:

```text
lint
typecheck
test
test:coverage
build
```

Add at least one meaningful smoke/component test so that the test infrastructure is genuinely exercised.

---

## Security

Create automated dependency audits.

Backend:

```text
pip-audit
```

Audit the dependencies represented by the uv project/lock file.

Frontend:

```text
pnpm audit
```

Treat high and critical vulnerabilities as CI failures.

---

## CodeQL

Prepare CodeQL analysis for:

```text
Python
JavaScript / TypeScript
```

CodeQL is intended for use when the repository is public or when the GitHub plan provides Code Security.

Do not introduce credentials for CodeQL.

---

## Dependabot

Configure Dependabot for:

```text
uv
npm/pnpm
GitHub Actions
```

Run version checks weekly.

Group minor and patch dependency updates where appropriate.

Do not group major updates with minor/patch updates.

---

## SonarQube Cloud

Create a SonarQube Cloud analysis workflow.

For the zero-cost configuration, run Sonar analysis on pushes to:

```text
main
```

Do not make the free Sonar analysis a required pull-request check if the active Sonar plan cannot analyze pull requests before merge.

Produce:

```text
backend/coverage.xml
frontend/coverage/lcov.info
```

when possible and expose them to Sonar.

The Sonar configuration must include both:

```text
backend/src
frontend/src
```

Exclude:

```text
virtual environments
node_modules
build output
coverage output
tool caches
```

Do not store the Sonar token in the repository.

The workflow must read:

```text
SONAR_TOKEN
```

from GitHub Actions secrets.

Use placeholders for repository-specific Sonar organization and project keys when they are not known.

---

## Pull requests

Create a pull request template containing:

```text
Summary
Changes
Testing
Quality & security
Screenshots
Architectural notes
Follow-up
```

The template must encourage explanations of why a change exists rather than merely summarizing the diff.

---

## Git workflow

Update `AGENTS.md` so coding agents are instructed to:

* develop changes on feature branches;
* avoid direct pushes to `main`;
* use Conventional Commit-style messages;
* inspect Git status and diff before finishing;
* run all relevant checks;
* never bypass a failing quality gate;
* never weaken tests merely to make CI pass;
* never merge a pull request without explicit user authorization;
* keep normal CI independent from real LLM credentials.

---

## Product engineering requirements

Update `SPEC.md` with non-functional quality requirements covering:

* pull-request development;
* protected `main`;
* automated CI;
* 80% backend coverage target;
* dependency vulnerability checks;
* Dependabot;
* SonarQube Cloud;
* CodeQL when available;
* secret management;
* deterministic tests.

---

## Local validation

Run all checks that can be run locally.

Backend:

```bash
uv run ruff check .
uv run mypy src
uv run pytest --cov=src/storybook --cov-report=term-missing
```

Frontend:

```bash
pnpm lint
pnpm typecheck
pnpm test:coverage
pnpm build
```

Review all workflow YAML files for syntax and path correctness.

---

## Constraints

Do not:

* add Docker solely for CI;
* introduce Jenkins or another CI platform;
* add paid infrastructure;
* call real LLMs from normal tests;
* commit secrets;
* commit generated coverage or frontend build directories;
* automatically merge pull requests;
* bypass existing Git protections.

Prefer GitHub-native capabilities.

---

## Expected result

After this task, the repository should be ready for this workflow:

```text
feature branch
      ↓
pull request
      ↓
backend CI
frontend CI
security checks
CodeQL when available
      ↓
merge
      ↓
main
      ↓
SonarQube Cloud analysis
```

All configuration must remain understandable to a developer reading the repository without external explanation.

