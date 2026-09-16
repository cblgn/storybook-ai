from functools import lru_cache
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from storybook.agents.writer import create_writer
from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook
from storybook.services.story_generator import StoryGenerationError, StoryGeneratorService
from storybook.settings import Settings

router = APIRouter()


@lru_cache
def get_story_service() -> StoryGeneratorService:
    settings = Settings()
    return StoryGeneratorService(create_writer(settings.model), settings.generation_timeout_seconds)


@router.post("/stories", response_model=StoryBook)
async def create_story(
    request: StoryRequest,
    service: Annotated[StoryGeneratorService, Depends(get_story_service)],
) -> StoryBook:
    try:
        return await service.generate(request)
    except StoryGenerationError:
        raise HTTPException(
            status_code=503,
            detail="Impossible de créer l'histoire pour le moment. Vous pouvez réessayer.",
        ) from None
