from abc import ABC, abstractmethod

from redis import Redis

from core.config import settings


class AbstractTokenHelper(ABC):

    @abstractmethod
    def get_user_password(self, username: str):
        pass

    @classmethod
    def verify_password(cls, password1: str, password2: str) -> bool:
        """
        password1 - password from database
        password2 - raw password
        """
        return password1 == password2

    def validate_user_password(self, username: str, password: str):
        password_db = self.get_user_password(username)
        if not password_db:
            return False
        return self.verify_password(password1=password_db, password2=password)


class RedisTokenHelper(AbstractTokenHelper):
    def __init__(
        self,
        host: str,
        port: int,
        redis_db: int,
    ):
        self.redis = Redis(
            host=host,
            port=port,
            decode_responses=True,
            db=redis_db,
        )

    def get_user_password(self, username):
        return self.redis.get(username)


redis_auth_helper = RedisTokenHelper(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    redis_db=settings.REDIS_USER_DB,
)
