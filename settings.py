from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class DataBaseSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    SECRET_KEY: str
    model_config = SettingsConfigDict(env_file=".env")

settings = DataBaseSettings()

def get_db_url():
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    )


class ApiSettings(BaseSettings):
    proxy_headers: bool
    server_header: bool
    access_log: bool
    model_config = SettingsConfigDict(env_file="apiconfig.env")
