from redis import Redis

from core.config import settings

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    db=settings.REDIS_DB_TOKENS,
)
