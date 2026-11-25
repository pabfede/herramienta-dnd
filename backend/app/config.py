from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DND_", env_file=".env", extra="ignore")

    data_dir: Path = Path("data")
    cors_origins: list[str] = ["http://localhost:5173"]

    @property
    def data_dir_resolved(self) -> Path:
        path = self.data_dir.resolve()
        path.mkdir(parents=True, exist_ok=True)
        return path


@lru_cache
def get_settings() -> Settings:
    return Settings()
