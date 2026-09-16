from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

StoryIngredient = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=300)
]


class StoryRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    child_name: str | None = Field(default=None, max_length=80)
    age: int = Field(default=7, ge=3, le=12, strict=True)
    hero: StoryIngredient
    setting: StoryIngredient
    theme: StoryIngredient
    duration_minutes: Literal[3, 5, 10] = 5
