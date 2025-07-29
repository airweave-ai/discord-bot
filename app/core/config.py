# app/core/config.py
from pydantic_settings import BaseSettings

from dotenv import load_dotenv
load_dotenv()
class DiscordSettings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    PUBLIC_KEY: str
    BOT_TOKEN: str
    API_VERSION: str = "v10"
    API_BASE_URL: str = "https://discord.com/api/v10"

    model_config = {
        "env_file": ".env",
        "env_prefix": "DISCORD_",
        "extra": "ignore"  # Ignore extra environment variables
    }
class RedisSettings(BaseSettings):
    HOST: str
    PORT: int
    DB: int = 0
    
    model_config = {
        "env_file": ".env",
        "env_prefix": "REDIS_",
        "extra": "ignore"  # Ignore extra environment variables
    }


class AppSettings(BaseSettings):
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_prefix": "APP_",
        "extra": "ignore"  # Ignore extra environment variables
    }
    
class Settings:
    def __init__(self):
        self.discord = DiscordSettings() # type: ignore
        self.redis = RedisSettings() # type: ignore
        self.app = AppSettings() # type: ignore


settings = Settings()  # type: ignore