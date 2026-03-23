from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os


ENV = os.getenv("ENVIRONMENT", "dev")


class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str = ""
    ENVIRONMENT: str = "dev"
    AUTH_PROVIDER: str = "supabase"

    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
