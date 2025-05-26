# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    discord_public_key: str
    discord_bot_token: str
    environment: str = "development"

    class Config:
        env_file = ".env"

settings = Settings()