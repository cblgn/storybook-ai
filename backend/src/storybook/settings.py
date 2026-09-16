from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STORYBOOK_", env_file=".env", extra="ignore")

    model: str = "openai-codex:gpt-5.6-luna"
    generation_timeout_seconds: float = Field(default=180, gt=0)
