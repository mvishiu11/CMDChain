"""
Configuration settings for the agent.
"""

from typing import Optional
import openai
from pydantic import BaseModel, field_validator, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class OpenAIConfig(BaseModel):
    """
    Settings for OpenAI API.

    Attributes:
        api_key (str): The OpenAI API key.
        model (str): The OpenAI model to use.
    """

    api_key: SecretStr
    model: Optional[str] = "gpt-3.5-turbo"

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, value):
        """
        Validates the OpenAI API key.
        """
        try:
            client = openai.OpenAI(api_key=value.get_secret_value())
            client.chat.completions.create(
                messages=[{"role": "user", "content": "Say this is a test"}],
                model="gpt-3.5-turbo",
                max_tokens=10,
            )
            return value
        except Exception as ex:
            raise ValueError(f"Invalid OpenAI API key: {ex}") from ex


class Settings(BaseSettings):
    """
    Application settings.

    Attributes:
        openai (Optional[OpenAIConfig]): The OpenAI settings.
        fastapi (Optional[FastAPIConfig]): The FastAPI settings.
        langsmith (Optional[LangSmithConfig]): The LangSmith settings (optional).
    """

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="APP_", env_nested_delimiter="__", extra="ignore"
    )

    openai: Optional[OpenAIConfig] = None

    @classmethod
    def load_settings(cls) -> "Settings":
        """
        Loads settings from environment variables or the .env file.
        Returns:
            Settings: The populated settings instance.
        """
        return cls()


settings = Settings.load_settings()
