import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="Dangerous_API_", env_file=".env")

    eddn_url: str = "tcp://eddn.edcd.io:9500"
    log_level: str = "INFO"
    embed_collector: bool = True
    database_url: str = (
        "postgresql+asyncpg://dangerous:dangerous@localhost:5432/dangerous"
    )
    secret = os.getenv("DANGEROUS_API_JWT_SECRET")
    if secret:
        jwt_secret: str = secret
    jwt_expires_in: int = 60


settings = Settings()
