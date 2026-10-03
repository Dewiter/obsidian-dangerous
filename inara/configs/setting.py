from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="INARA_", env_file=".env")

    eddn_url: str = "tcp://eddn.edcd.io:9500"
    log_level: str = "INFO"
    embed_collector: bool = True


settings = Settings()
