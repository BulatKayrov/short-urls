import logging
from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DB_FILE: Path = BASE_DIR / "shorts.json"

    # logging
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # jwt
    API_TOKENS: frozenset[str] = frozenset(
        {"aK1J-Ez_gQc4iHh8Pa6J-w", "vHOm99YdSFO7c3PuIA6guQ"}
    )

    USER_DB: dict[str, str] = {
        "1": "1",
    }

    # redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6666


settings = Settings()
