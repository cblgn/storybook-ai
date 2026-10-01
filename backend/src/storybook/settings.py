from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="STORYBOOK_", env_file=".env", extra="ignore")

    model: str = "ollama:qwen3.5:0.8b"
    ollama_base_url: str = "http://127.0.0.1:11434/v1"
    generation_timeout_seconds: float = Field(default=180, gt=0)
