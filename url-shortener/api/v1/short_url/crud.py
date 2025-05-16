from logging import getLogger

from pydantic import BaseModel, ValidationError
from redis import Redis

from api.v1.short_url.schemas import (
    SCreateShortUrl,
    SUpdatePathShortUrl,
    SUpdateShortUrl,
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


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def init_storage(self) -> None:
        try:
            data = ShortUrlsStorage.from_statement()
        except ValidationError:
            self.save()
            logger.warning("ShortUrlsStorage reloaded")
            return

        self.slug_to_short_url.update(data.slug_to_short_url)
        logger.warning("ShortUrlsStorage loaded")

    def save(self):
        settings.DB_FILE.write_text(self.model_dump_json(indent=4))
        logger.debug("Saved short url schema")

    @classmethod
    def from_statement(cls):
        if not settings.DB_FILE.exists():
            return ShortUrlsStorage()
        return cls.model_validate_json(settings.DB_FILE.read_text())

    def get(self):
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug):
        return self.slug_to_short_url.get(slug)

    def create(self, data: SCreateShortUrl):
        short_url = ShortUrl(**data.model_dump())
        redis_helper.hset(
            name=settings.REDIS_SHORT_URL_HASH_NAME,
            key=short_url.slug,
            value=short_url.model_dump_json(),
        )
        logger.info("Created short url %s", short_url.slug)
        return short_url

    def delete_by_slug(self, slug):
        self.slug_to_short_url.pop(slug, None)

    def delete_short_url(self, short_url: ShortUrl):
        self.delete_by_slug(slug=short_url.slug)

    def update_by_slug(self, short_url: ShortUrl, short_url_in: SUpdateShortUrl):
        for name, value in short_url_in:
            setattr(short_url, name, value)

        return short_url

    def partial_update(self, short_url: ShortUrl, short_url_in: SUpdatePathShortUrl):
        for name, value in short_url_in.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            setattr(short_url, name, value)

        return short_url

    def update_short(
        self,
        short_url: ShortUrl,
        short_url_in: SUpdatePathShortUrl,
        partial: bool = False,
    ):
        for name, value in short_url_in.model_dump(
            exclude_none=partial, exclude_unset=partial
        ).items():
            setattr(short_url, name, value)

        return short_url


storage = ShortUrlsStorage()
storage.init_storage()
