import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from pydantic_ai import models
from pydantic_ai.models.test import TestModel

from storybook.agents.writer import create_writer
from storybook.api.app import app
from storybook.api.routes.stories import get_story_service
from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook
from storybook.services.story_generator import StoryGeneratorService


@pytest.fixture(autouse=True)
def prevent_real_llm_requests(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(models, "ALLOW_MODEL_REQUESTS", False)


@pytest.fixture
def story() -> StoryBook:
    data = json.loads((Path(__file__).parent / "fixtures/story.json").read_text())
    return StoryBook.model_validate(data)


@pytest.fixture
def story_request() -> StoryRequest:
    return StoryRequest(
        child_name="Léa",
        age=6,
        hero="un petit dragon timide",
        setting="forêt enchantée",
        theme="prendre confiance en soi",
        duration_minutes=3,
    )


@pytest.fixture
def service(story: StoryBook) -> StoryGeneratorService:
    return StoryGeneratorService(create_writer(TestModel(custom_output_args=story.model_dump())))


@pytest.fixture
def client(service: StoryGeneratorService) -> Iterator[TestClient]:
    app.dependency_overrides[get_story_service] = lambda: service
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
