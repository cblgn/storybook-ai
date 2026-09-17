import json
from collections.abc import AsyncIterator

import httpx
import pytest
from pydantic_ai import models
from pydantic_ai.providers.ollama import OllamaProvider

from storybook.agents.writer import create_writer
from storybook.api.routes.stories import get_story_service
from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook
from storybook.services.story_generator import StoryGenerationError, StoryGeneratorService
from storybook.settings import Settings


@pytest.fixture
async def ollama_requests(
    monkeypatch: pytest.MonkeyPatch, story: StoryBook, request: pytest.FixtureRequest
) -> AsyncIterator[list[httpx.Request]]:
    requests: list[httpx.Request] = []
    outcome = getattr(request, "param", "success")

    def respond(incoming: httpx.Request) -> httpx.Response:
        requests.append(incoming)
        if outcome == "missing-model":
            return httpx.Response(404, json={"error": {"message": "model not found"}})
        content = story.model_dump_json() if outcome == "success" else '{"title":"Incomplete"}'
        return httpx.Response(
            200,
            json={
                "id": "test-completion",
                "object": "chat.completion",
                "created": 0,
                "model": "qwen3.5:0.8b",
                "choices": [
                    {
                        "index": 0,
                        "finish_reason": "stop",
                        "message": {"role": "assistant", "content": content},
                    }
                ],
            },
        )

    async with httpx.AsyncClient(transport=httpx.MockTransport(respond)) as client:

        def mock_provider(*, base_url: str, api_key: str) -> OllamaProvider:
            return OllamaProvider(base_url=base_url, api_key=api_key, http_client=client)

        monkeypatch.setattr("storybook.agents.writer.OllamaProvider", mock_provider)
        # Only this adapter test can make requests, through the in-memory transport.
        with models.override_allow_model_requests(True):
            yield requests


async def test_local_writer_uses_native_schema_and_configured_endpoint(
    ollama_requests: list[httpx.Request],
    story_request: StoryRequest,
    story: StoryBook,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("STORYBOOK_MODEL", "ollama:qwen3.5:0.8b")
    monkeypatch.setenv("STORYBOOK_OLLAMA_BASE_URL", "http://ollama.test:11434/v1")
    get_story_service.cache_clear()
    try:
        result = await get_story_service().generate(story_request)
    finally:
        get_story_service.cache_clear()
    assert result == story
    assert len(ollama_requests) == 1
    incoming = ollama_requests[0]
    assert str(incoming.url) == "http://ollama.test:11434/v1/chat/completions"
    body = json.loads(incoming.content)
    assert body["model"] == "qwen3.5:0.8b"
    assert body["reasoning_effort"] == "none"
    assert body["response_format"]["type"] == "json_schema"
    schema = body["response_format"]["json_schema"]["schema"]
    assert set(schema["required"]) == set(StoryBook.model_fields)
    assert not body.get("tools")
    assert json.loads(body["messages"][-1]["content"]) == story_request.model_dump()


@pytest.mark.parametrize("ollama_requests", ["invalid-output", "missing-model"], indirect=True)
async def test_local_writer_rejects_invalid_output_and_provider_errors(
    ollama_requests: list[httpx.Request],
    story_request: StoryRequest,
) -> None:
    service = StoryGeneratorService(create_writer("ollama:qwen3.5:0.8b"))
    with pytest.raises(StoryGenerationError, match="^Story generation failed$"):
        await service.generate(story_request)
    assert 1 <= len(ollama_requests) <= 2
    assert all(incoming.url.host == "127.0.0.1" for incoming in ollama_requests)


def test_default_provider_needs_no_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in (
        "STORYBOOK_MODEL",
        "STORYBOOK_OLLAMA_BASE_URL",
        "OPENAI_API_KEY",
        "OLLAMA_API_KEY",
    ):
        monkeypatch.delenv(name, raising=False)
    settings = Settings(_env_file=None)
    assert settings.model == "ollama:qwen3.5:0.8b"
    assert settings.ollama_base_url == "http://127.0.0.1:11434/v1"
    create_writer(settings.model, ollama_base_url=settings.ollama_base_url)


@pytest.mark.integration
async def test_real_local_qwen(story_request: StoryRequest) -> None:
    """Explicit opt-in: requires a local Ollama server and the downloaded model."""
    writer = create_writer("ollama:qwen3.5:0.8b")
    with models.override_allow_model_requests(True):
        story = await StoryGeneratorService(writer).generate(story_request)
    assert isinstance(story, StoryBook)
    assert story.scenes
