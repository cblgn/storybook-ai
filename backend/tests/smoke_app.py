"""Browser-test server: real HTTP/service/agent with a deterministic model, no LLM calls."""

from pathlib import Path

from pydantic_ai import models
from pydantic_ai.models.test import TestModel

from storybook.agents.writer import create_writer
from storybook.api.app import app
from storybook.api.routes.stories import get_story_service
from storybook.domain.stories import StoryBook
from storybook.services.story_generator import StoryGeneratorService

models.ALLOW_MODEL_REQUESTS = False
story = StoryBook.model_validate_json((Path(__file__).parent / "fixtures/story.json").read_text())
service = StoryGeneratorService(create_writer(TestModel(custom_output_args=story.model_dump())))
app.dependency_overrides[get_story_service] = lambda: service
