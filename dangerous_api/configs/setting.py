from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Host
    host_app_name: str = "Dangerous API"
    host_mode: str = "development"
    host_address: str = "localhost"
    host_port: int = 8000
    app_prefix: str = ""

    # Logging
    log_level: str = "INFO"

    # Application
    embed_collector: bool = True

    # EDDN
    eddn_net: str = "tcp"
    eddn_host: str = "eddn.edcd.io"
    eddn_port: int = 9500

    # Database (no defaults: credentials must come from .env)
    db_net: str
    db_host: str
    db_port: int
    db_base: str

    # JWT
    jwt_secret: str
    jwt_duration: int = 60  # minutes
    jwt_refresh: int = 90  # unused for now

    @property
    def eddn_url(self) -> str:
        return f"{self.eddn_net}://{self.eddn_host}:{self.eddn_port}"

    @property
    def database_url(self) -> str:
        return f"{self.db_net}://{self.db_host}:{self.db_port}{self.db_base}"


settings = Settings()
