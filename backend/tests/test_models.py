import pytest
from pydantic import ValidationError

from storybook.domain.requests import StoryRequest
from storybook.domain.stories import StoryBook


@pytest.mark.parametrize(
    "field,value",
    [
        ("age", 2),
        ("age", 13),
        ("age", 6.5),
        ("age", True),
        ("duration_minutes", 4),
        ("hero", "  "),
        ("theme", ""),
        ("setting", "x" * 301),
        ("child_name", "x" * 81),
    ],
)
def test_invalid_request(story_request: StoryRequest, field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        StoryRequest.model_validate({**story_request.model_dump(), field: value})


def test_defaults_and_whitespace() -> None:
    request = StoryRequest(hero="  un dragon  ", setting="la forêt", theme="le courage")
    assert request.child_name is None
    assert request.age == 7
    assert request.duration_minutes == 5
    assert request.hero == "un dragon"


@pytest.mark.parametrize("field,value", [("scenes", []), ("characters", []), ("title", " ")])
def test_empty_story_rejected(story: StoryBook, field: str, value: object) -> None:
    with pytest.raises(ValidationError):
        StoryBook.model_validate({**story.model_dump(), field: value})
