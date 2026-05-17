from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application related variables
    APP_TITLE: str = "Ephemeris API"
    APP_DESCRIPTION: str = "Open Swiss Ephemeris REST API"
    APP_VERSION: str = "0.1.0"

    # Runtime defaults
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Swiss Ephemeris download path
    EPHE_PATH: str = "./ephe"

    model_config = SettingsConfigDict(env_file=".env")


@cache
def get_settings() -> Settings:
    return Settings()
