import logging
from pathlib import Path

from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # logging
    LOG_LEVEL: int = logging.INFO
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6666
    REDIS_DB_TOKENS: int = 1
    REDIS_TOKENS_SET_NAME: str = "tokens"
    REDIS_USER_DB: int = 2
    REDIS_SHORT_URL: int = 0
    REDIS_SHORT_URL_HASH_NAME: str = "short_url"

    # tests
    TEST_REDIS_HOST: str = "localhost"
    TEST_REDIS_PORT: int = 1234
    TEST_REDIS_DB: int = 0
    TEST_REDIS_SHORT_URL: int = 1
    TEST_TOKENS_SET_NAME: str = "tokens"


settings = Settings()
