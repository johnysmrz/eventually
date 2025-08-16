from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = Field("localhost")
    JWT_SECRET_KEY: str
    BASE_URL: str

@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore
