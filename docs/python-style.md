# Python style examples

[AGENTS.md](../AGENTS.md#python-coding-standards) defines the permanent rules.
This guide illustrates them for Python changes; it does not require restyling
unrelated code. Read the backend [configuration](../backend/pyproject.toml) for
the targeted Python version and quality tools, and
[CONTRIBUTING.md](../CONTRIBUTING.md#vérifications-locales) for validation commands.

## Typing and metadata

Use ordinary annotations for ordinary data. A named alias is useful when it
clarifies a shared contract, for example:

```python
from typing import Literal

type ReadingDuration = Literal[3, 5, 10]

name: str
names: list[str]
child_name: str | None
```

Use `Annotated` when validation or framework metadata belongs with the type.
The existing [request models](../backend/src/storybook/domain/requests.py) use
this pattern for shared string constraints:

```python
from typing import Annotated

from pydantic import StringConstraints

StoryIngredient = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)
]
```

FastAPI dependency metadata belongs in the annotation, as in the existing
[story route](../backend/src/storybook/api/routes/stories.py):

```python
async def create_story(
    request: StoryRequest,
    service: Annotated[StoryGeneratorService, Depends(get_story_service)],
) -> StoryBook:
    ...
```

The same principle applies to query, path, header, cookie and body metadata.
Do not wrap plain types in `Annotated` with placeholder metadata. A one-off
model field can retain `Field(...)` on the assignment; shared constraints are a
reason to introduce a reusable annotated type, not to convert every field.

## Pydantic

Use `model_validate` for validation, `model_dump` for serialization and
`model_config` for model configuration. When custom validation is needed, use
`field_validator`, `model_validator` or an annotated validator at the relevant
type boundary. Do not introduce Pydantic v1 APIs.

Prefer existing declarative constraints to a custom validator that does the
same work. Model validation remains deterministic Python, independently of
instructions sent to an LLM.

## Readability and boundaries

- Keep functions cohesive and dependencies explicit. Use early returns and
  comprehensions when they make control flow easier to read.
- Use `pathlib.Path` for paths and context managers for resources. Prefer the
  standard library before adding dependencies.
- Use enums for closed sets of values, and immutable or read-only contracts
  when mutation would violate an actual invariant.
- Avoid mutable defaults. A boolean argument is acceptable when its meaning is
  clear; prefer a descriptive keyword or a more explicit operation otherwise.
- A concrete type is often sufficient. Introduce a `Protocol` for a needed
  structural contract, without speculative inheritance or wrapper classes.
- A broad exception handler needs a specific boundary rationale. For example,
  the [generation service](../backend/src/storybook/services/story_generator.py)
  translates provider failures and retains their cause; the HTTP boundary
  returns a sanitized error rather than exposing provider details.
- Fix typing problems at their source. If a dependency limitation requires a
  suppression, identify the narrow error code and document the reason beside
  it; do not suppress a whole file or weaken the configured checks.
