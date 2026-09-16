# Storybook AI — MVP Specification

## 1. Product vision

Storybook AI is a web application that creates personalized children's stories using an LLM.

A parent provides a few ingredients:

* child's name;
* child's age;
* hero;
* setting;
* theme;
* desired duration.

The application creates a coherent, personalized, age-appropriate story.

The product should feel like a small finished web application rather than an LLM playground.

---

# 2. Project constraints

The MVP must:

* run locally;
* require no paid hosting;
* require no cloud infrastructure;
* use a real React frontend;
* use FastAPI as its backend;
* use PydanticAI for the LLM integration;
* use an LLM as a core part of the product;
* be maintainable in a single Git repository;
* be achievable as a one-day MVP.

The project must not depend on having a powerful local GPU.

---

# 3. Repository

The project is maintained as a Git monorepo.

Expected top-level structure:

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

Frontend and backend belong to the same repository because they implement a single product and evolve together.

---

# 4. Primary objective

The MVP demonstrates this complete AI-native workflow:

```text
User input
    ↓
Story planning
    ↓
Story writing
    ↓
AI review
    ↓
Optional revision
    ↓
Story displayed in browser
```

The LLM is part of the application's core business logic.

Without the LLM, the primary functionality does not exist.

---

# 5. Target user

The primary user is a parent who wants to quickly create a personalized bedtime story for a child.

No user account is required.

---

# 6. Main user story

As a parent,

I want to provide a few ideas about my child and the desired story,

so that the application generates a personalized story appropriate for the child's age.

---

# 7. Main screen

The initial product has one main page.

Desktop layout:

```text
┌─────────────────────────────────────────────────────┐
│                   Storybook AI                      │
│         Une histoire rien que pour vous ✨          │
│                                                     │
│  ┌─────────────────────┐ ┌───────────────────────┐ │
│  │                     │ │                       │ │
│  │ Story configuration │ │ Generated story       │ │
│  │                     │ │                       │ │
│  │ ...                 │ │ ...                   │ │
│  │                     │ │                       │ │
│  └─────────────────────┘ └───────────────────────┘ │
└─────────────────────────────────────────────────────┘
```

On smaller screens, the two sections stack vertically.

---

# 8. Story creation form

## Child name

Optional.

Example:

```text
Léa
```

The child's name may be incorporated into the story when appropriate.

---

## Age

Required.

Allowed range:

```text
3–12
```

Default:

```text
7
```

Age influences:

* vocabulary;
* sentence complexity;
* themes;
* amount of explanation;
* narrative complexity.

---

## Hero

Required free-text field.

Example:

```text
Un petit dragon timide
```

---

## Setting

Required.

Suggested values may include:

* forêt enchantée;
* espace;
* pirates;
* dinosaures;
* monde sous-marin;
* château médiéval.

The user may also provide another setting.

---

## Theme

Required.

Examples:

* courage;
* friendship;
* sharing;
* patience;
* fear of the dark;
* curiosity;
* self-confidence.

---

## Duration

Required.

Available values:

```text
3 minutes
5 minutes
10 minutes
```

Default:

```text
5 minutes
```

Duration is an approximate reading duration rather than an exact timing guarantee.

---

# 9. Story generation

The primary action is:

```text
Créer l'histoire
```

Submitting the form triggers the backend AI workflow.

The user must not be able to accidentally submit the same generation multiple times while a request is already running.

---

# 10. AI stage 1 — Planning

A planner agent receives `StoryRequest`.

It produces a structured `StoryPlan`.

Conceptually:

```python
class StoryPlan(BaseModel):
    title: str
    premise: str
    characters: list[Character]
    setting: str
    challenge: str
    key_events: list[str]
    resolution: str
    theme: str
```

The planner determines the narrative structure.

It does not produce the final prose.

The plan remains internal for the MVP.

---

# 11. Characters

Characters should have a structured representation.

Conceptually:

```python
class Character(BaseModel):
    name: str
    description: str
    personality: list[str]
```

Character traits should remain consistent during the story.

---

# 12. AI stage 2 — Writing

The writer receives:

```text
StoryRequest
+
StoryPlan
```

and produces a typed `StoryBook`.

Conceptually:

```python
class StoryScene(BaseModel):
    title: str
    text: str


class StoryBook(BaseModel):
    title: str
    synopsis: str
    characters: list[Character]
    scenes: list[StoryScene]
    closing_sentence: str
```

---

# 13. Writing requirements

The initial MVP generates stories in French.

Stories must:

* suit the child's age;
* respect the requested hero;
* respect the requested setting;
* address the requested theme;
* approximately respect the requested duration;
* use appropriate vocabulary;
* preserve character consistency;
* contain a clear beginning;
* contain narrative development;
* contain a resolution;
* avoid unnecessarily frightening or disturbing content;
* end positively or reassuringly.

---

# 14. AI stage 3 — Review

A reviewer evaluates the generated `StoryBook`.

It produces a typed `StoryReview`.

Conceptually:

```python
class StoryReview(BaseModel):
    age_appropriate: bool
    coherent: bool
    characters_consistent: bool
    theme_respected: bool
    positive_ending: bool

    issues: list[str]
    revision_needed: bool
```

---

# 15. Automatic revision

If:

```python
revision_needed is True
```

the writer may receive:

```text
StoryBook
+
StoryReview
```

and generate a corrected version.

Only one automatic revision is allowed.

The workflow must always terminate.

---

# 16. API

The initial API exposes:

```http
POST /api/stories
GET /api/health
```

---

# 17. Story request

Example:

```json
{
  "child_name": "Léa",
  "age": 6,
  "hero": "un petit dragon timide",
  "setting": "forêt enchantée",
  "theme": "prendre confiance en soi",
  "duration_minutes": 5
}
```

---

# 18. Story response

Example:

```json
{
  "title": "Zéphyr et la forêt aux mille lumières",
  "synopsis": "Zéphyr découvre qu'il peut être courageux même lorsqu'il a peur.",
  "characters": [
    {
      "name": "Zéphyr",
      "description": "Un petit dragon bleu",
      "personality": [
        "timide",
        "curieux",
        "gentil"
      ]
    }
  ],
  "scenes": [
    {
      "title": "Une lumière étrange",
      "text": "..."
    },
    {
      "title": "Au cœur de la forêt",
      "text": "..."
    },
    {
      "title": "Le courage de Zéphyr",
      "text": "..."
    }
  ],
  "closing_sentence": "Et cette nuit-là, Zéphyr s'endormit en sachant qu'être courageux ne voulait pas dire ne jamais avoir peur."
}
```

---

# 19. Loading state

During generation, the interface must clearly indicate that work is in progress.

Minimum:

```text
✨ Création de votre histoire...
```

A spinner, skeleton, or progress indicator may be used.

Exact agent progress reporting is not required for the initial MVP.

---

# 20. Story display

The completed story should be presented as readable long-form content.

Display:

```text
Title

Synopsis

Scene 1
...

Scene 2
...

Closing sentence
```

Readable typography has priority over dense information presentation.

---

# 21. New story

Once a story has been generated, the user can create another story.

No conversational chat interface is required.

---

# 22. Errors

Generation errors must result in a friendly frontend message.

Example:

```text
Impossible de créer l'histoire pour le moment.

Vous pouvez réessayer.
```

Never expose:

* Python tracebacks;
* raw LLM provider errors;
* credentials;
* internal prompts.

---

# 23. Frontend

Use:

* React;
* TypeScript;
* Vite;
* Tailwind CSS;
* shadcn/ui.

The application must be responsive.

No server-side rendering is necessary.

---

# 24. Backend

Use:

* Python 3.14+;
* FastAPI;
* Pydantic v2;
* PydanticAI;
* uv.

The LLM provider must remain configurable.

Credentials must stay outside Git.

---

# 25. Development topology

During development:

```text
Browser
   │
   ▼
React / Vite :5173
   │
   │ /api
   ▼
FastAPI :8000
   │
   ▼
StoryGeneratorService
   │
   ├── Planner
   ├── Writer
   └── Reviewer
          │
          ▼
      PydanticAI
          │
          ▼
          LLM
```

---

# 26. Production-like local build

The React frontend must support:

```bash
pnpm build
```

A later step may make FastAPI serve the generated static frontend.

The desired final local experience is eventually:

```bash
uv run storybook
```

followed by opening one local URL.

This single-process packaging is desirable but lower priority than completing the main workflow.

---

# 27. Persistence

Persistence is not required for the first MVP.

Reloading the page may lose the generated story.

If persistence is added after the core MVP works, prefer JSON files:

```text
data/
└── stories/
    └── <story-id>.json
```

A database is not justified for the initial scope.

---

# 28. Git

The repository must be initialized before implementation begins.

The initial branch is:

```text
main
```

The initial project setup should create a `.gitignore` appropriate for both Python and Node development.

Credentials, dependencies, caches, generated builds, and local story data must not be tracked.

Commits are useful checkpoints but should not block rapid MVP development.

Codex must not create commits unless explicitly requested.

---

# 29. Repository documentation

The repository should contain:

```text
README.md
AGENTS.md
SPEC.md
TASKS/
```

`README.md` explains how a human developer runs the project.

`SPEC.md` contains product requirements.

`AGENTS.md` contains stable development instructions for coding agents.

`TASKS/` records significant implementation missions.

---

# 30. Explicitly out of scope

The initial version does not include:

* authentication;
* user accounts;
* AWS;
* cloud hosting;
* database;
* Redis;
* Celery;
* payments;
* image generation;
* audio narration;
* speech synthesis;
* story sharing;
* email;
* persistent fictional worlds;
* recurring character libraries;
* multilingual generation;
* mobile application.

---

# 31. Acceptance criteria

The MVP is complete when:

1. the project exists as a Git repository;

2. frontend and backend live in the same repository;

3. the web application opens in a browser;

4. the user can provide:

   * age;
   * hero;
   * setting;
   * theme;
   * duration;

5. React sends the request to FastAPI;

6. PydanticAI invokes an LLM;

7. the planner produces a structured `StoryPlan`;

8. the writer produces a structured `StoryBook`;

9. the reviewer evaluates it;

10. no more than one revision occurs;

11. FastAPI returns the final story;

12. React displays it cleanly;

13. errors are handled cleanly;

14. backend tests pass;

15. backend linting and type checks pass;

16. the React production build succeeds;

17. Git contains no credentials or generated dependency directories.

---

# 32. Implementation priority

When time is constrained, work in this order:

```text
1. Initialize Git repository
2. Create repository skeleton
3. Configure backend tooling
4. Configure frontend tooling
5. Create Pydantic domain models
6. Implement Writer agent
7. Expose POST /api/stories
8. Create React form
9. Render generated story
10. Add Planner
11. Add Reviewer
12. Add single revision
13. Improve visual design
14. Improve local packaging
15. Add optional persistence
```

End-to-end functionality has priority over architectural completeness.

---

# 33. Success scenario

The developer starts the backend and frontend.

The browser displays Storybook AI.

The user enters:

```text
Léa
6 ans
Un petit dragon timide
Une forêt enchantée
Apprendre à avoir confiance en soi
5 minutes
```

The user clicks:

```text
Créer l'histoire
```

The application generates, reviews, and displays a complete personalized story.

That is the MVP.
