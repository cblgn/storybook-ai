from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook
from storybook.services.story_generator import StoryGeneratorService


def test_health(client: TestClient) -> None:
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_story_api(client: TestClient, story_request: StoryRequest, story: StoryBook) -> None:
    response = client.post("/api/stories", json=story_request.model_dump())
    assert response.status_code == 200
    assert response.json() == story.model_dump()


def test_invalid_input_never_calls_writer(
    client: TestClient,
    service: StoryGeneratorService,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    run = AsyncMock()
    monkeypatch.setattr(service.writer, "run", run)
    response = client.post("/api/stories", json={"age": 2})
    assert response.status_code == 422
    run.assert_not_called()


def test_errors_do_not_expose_provider_details(
    client: TestClient,
    service: StoryGeneratorService,
    story_request: StoryRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(service.writer, "run", AsyncMock(side_effect=RuntimeError("secret-token")))
    response = client.post("/api/stories", json=story_request.model_dump())
    assert response.status_code == 503
    assert "Vous pouvez réessayer" in response.json()["detail"]
    assert "secret-token" not in response.text
