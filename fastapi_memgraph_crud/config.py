from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI Memgraph CRUD"
    app_debug: bool = True

    memgraph_host: str = "localhost"
    memgraph_port: int = 7687
    memgraph_username: str = ""
    memgraph_password: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
