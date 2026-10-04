from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    # Host
    host_app_name: str
    host_mode: str
    host_address: str
    host_port: int
    app_prefix: str

    # Logging
    log_level: str = "INFO"

    # Application
    embed_collector: bool = True

    # EDDN
    eddn_host: str
    eddn_net: str
    eddn_port: int

    # Database
    db_host: str
    db_port: int
    db_net: str
    db_base: str

    # JWT
    jwt_secret: str | None = None
    jwt_duration: int = 60
    jwt_refresh: int = 90

    @computed_field
    @property
    def eddn_url(self) -> str:
        return f"{self.eddn_net}://{self.eddn_host}:{self.eddn_port}"

    @computed_field
    @property
    def database_url(self) -> str:
        return f"{self.db_net}://{self.db_host}:{self.db_port}{self.db_base}"


settings = Settings()
