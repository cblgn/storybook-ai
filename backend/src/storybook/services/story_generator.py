import asyncio

from pydantic_ai import Agent
from pydantic_ai.usage import UsageLimits

from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook


class StoryGenerationError(Exception):
    """Story generation failed or exceeded its time budget."""


class StoryGeneratorService:
    def __init__(self, writer: Agent[None, StoryBook], timeout_seconds: float = 180) -> None:
        self.writer = writer
        self.timeout_seconds = timeout_seconds

    async def generate(self, request: StoryRequest) -> StoryBook:
        try:
            async with asyncio.timeout(self.timeout_seconds):
                result = await self.writer.run(
                    request.model_dump_json(), usage_limits=UsageLimits(request_limit=3)
                )
            return result.output
        except Exception as exc:
            # Translate provider/configuration failures without exposing their content.
            raise StoryGenerationError("Story generation failed") from exc
