from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

NonEmptyText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]


class Character(BaseModel):
    name: NonEmptyText
    description: NonEmptyText
    personality: list[NonEmptyText] = Field(min_length=1)


class StoryScene(BaseModel):
    title: NonEmptyText
    text: NonEmptyText


class StoryBook(BaseModel):
    title: NonEmptyText
    synopsis: NonEmptyText
    characters: list[Character] = Field(min_length=1)
    scenes: list[StoryScene] = Field(min_length=1)
    closing_sentence: NonEmptyText
