from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DB_FILE: Path = BASE_DIR / "shorts.json"


settings = Settings()
