from logging import getLogger

from fastapi import HTTPException
from redis import Redis

from api.v1.short_url.schemas import (
    SCreateShortUrl,
    SUpdatePathShortUrl,
    ShortUrl,
)
from core.config import settings

logger = getLogger(__name__)

redis_helper = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_SHORT_URL,
    decode_responses=True,
)


class ShortUrlsStorage:

    @classmethod
    def save(cls, short_url):
        redis_helper.hset(
            name=settings.REDIS_SHORT_URL_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    @classmethod
    def get(cls):
        result = redis_helper.hvals(name=settings.REDIS_SHORT_URL_HASH_NAME)
        return [ShortUrl.model_validate_json(item) for item in result] if result else []

    @classmethod
    def get_by_slug(cls, slug):
        obj = redis_helper.hget(name=settings.REDIS_SHORT_URL_HASH_NAME, key=slug)
        if obj:
            return ShortUrl.model_validate_json(json_data=obj)
        return HTTPException(status_code=404, detail="Not found")

    @classmethod
    def create(cls, data: SCreateShortUrl | ShortUrl):
        short_url = ShortUrl(**data.model_dump())
        if not cls.get_by_slug(short_url.slug):
            cls.save(short_url)
            logger.info("Created short url %s", short_url.slug)
            return short_url
        raise HTTPException(status_code=404, detail="Short url already exists")

    @classmethod
    def delete_by_slug(cls, slug) -> None:
        redis_helper.hdel(settings.REDIS_SHORT_URL_HASH_NAME, slug)

    @classmethod
    def delete_short_url(cls, short_url: ShortUrl):
        cls.delete_by_slug(slug=short_url.slug)

    @classmethod
    def update_short(
        cls,
        short_url: ShortUrl,
        short_url_in: SUpdatePathShortUrl,
        partial: bool = False,
    ):
        # obj = cls.get_by_slug(slug=short_url.slug)
        for name, value in short_url_in.model_dump(
            exclude_none=partial, exclude_unset=partial
        ).items():
            setattr(short_url, name, value)
        cls.save(short_url)
        return short_url


storage = ShortUrlsStorage()
