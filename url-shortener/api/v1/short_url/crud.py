from logging import getLogger

from fastapi import HTTPException
from redis import Redis

from api.v1.short_url.schemas import (
    SCreateShortUrl,
    ShortUrl,
    SUpdatePathShortUrl,
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

    def save(self, short_url: ShortUrl) -> None:
        redis_helper.hset(
            name=settings.REDIS_SHORT_URL_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )

    def get(self) -> list[ShortUrl]:
        result = redis_helper.hvals(name=settings.REDIS_SHORT_URL_HASH_NAME)
        return [ShortUrl.model_validate_json(item) for item in result] if result else []

    def get_by_slug(self, slug: str) -> str | None:
        return redis_helper.hget(name=settings.REDIS_SHORT_URL_HASH_NAME, key=slug)

    def create(self, data: SCreateShortUrl | ShortUrl) -> ShortUrl:
        short_url = ShortUrl(**data.model_dump())
        if not self.get_by_slug(short_url.slug):
            self.save(short_url)
            logger.info("Created short url %s", short_url.slug)
            return short_url
        raise HTTPException(status_code=404, detail="Short url already exists")

    def delete_by_slug(self, slug: str) -> None:
        redis_helper.hdel(settings.REDIS_SHORT_URL_HASH_NAME, slug)

    def delete_short_url(self, short_url: ShortUrl) -> None:
        self.delete_by_slug(slug=short_url.slug)

    def update_short(
        self,
        short_url: ShortUrl,
        short_url_in: SUpdatePathShortUrl,
        partial: bool = False,
    ) -> ShortUrl:
        for name, value in short_url_in.model_dump(
            exclude_none=partial, exclude_unset=partial
        ).items():
            setattr(short_url, name, value)
        self.save(short_url)
        return short_url


storage = ShortUrlsStorage()
