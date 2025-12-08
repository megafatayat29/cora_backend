from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    NEO4J_URI: str = "neo4j://mentorku.cloud:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "xsw21qaz"

    HF_TOKEN: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  # agar tidak error jika ada variable lain
    )

@lru_cache()
def get_settings():
    return Settings()