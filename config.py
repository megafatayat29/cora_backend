from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NEO4J_URI: str = "neo4j://mentorku.cloud:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "xsw21qaz"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
