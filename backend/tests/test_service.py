import asyncio
import json
from unittest.mock import AsyncMock

import pytest
from pydantic_ai import capture_run_messages
from pydantic_ai.messages import ModelRequest, UserPromptPart
from pydantic_ai.models.test import TestModel

from storybook.agents.writer import create_writer
from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook
from storybook.services.story_generator import StoryGenerationError, StoryGeneratorService


async def test_writer_receives_request_and_returns_typed_story(
    service: StoryGeneratorService,
    story_request: StoryRequest,
    story: StoryBook,
) -> None:
    with capture_run_messages() as messages:
        result = await service.generate(story_request)
    assert result == story
    prompts = [
        part.content
        for message in messages
        if isinstance(message, ModelRequest)
        for part in message.parts
        if isinstance(part, UserPromptPart)
    ]
    assert json.loads(str(prompts[0])) == story_request.model_dump()


async def test_provider_failure_is_translated(
    service: StoryGeneratorService,
    story_request: StoryRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        service.writer, "run", AsyncMock(side_effect=RuntimeError("private detail"))
    )
    with pytest.raises(StoryGenerationError, match="^Story generation failed$"):
        await service.generate(story_request)


async def test_timeout_is_bounded(
    service: StoryGeneratorService,
    story_request: StoryRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    service.timeout_seconds = 0.01

    async def slow_run(*args: object, **kwargs: object) -> None:
        await asyncio.sleep(10)

    monkeypatch.setattr(service.writer, "run", slow_run)
    with pytest.raises(StoryGenerationError) as exc:
        await service.generate(story_request)
    assert isinstance(exc.value.__cause__, TimeoutError)


async def test_invalid_model_output_is_rejected(story_request: StoryRequest) -> None:
    writer = create_writer(TestModel(custom_output_args={"title": "Incomplete"}))
    with pytest.raises(StoryGenerationError):
        await StoryGeneratorService(writer).generate(story_request)
