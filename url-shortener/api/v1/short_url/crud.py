from logging import getLogger

from pydantic import BaseModel, ValidationError

from api.v1.short_url.schemas import (
    ShortUrl,
    SCreateShortUrl,
    SUpdateShortUrl,
    SUpdatePathShortUrl,
)
from core.config import settings

logger = getLogger(__name__)


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

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
        self.slug_to_short_url[short_url.slug] = short_url
        self.save()
        logger.info("Created short url %s", short_url.slug)
        return short_url

    def delete_by_slug(self, slug):
        self.slug_to_short_url.pop(slug, None)
        self.save()

    def delete_short_url(self, short_url: ShortUrl):
        self.delete_by_slug(slug=short_url.slug)

    def update_by_slug(self, short_url: ShortUrl, short_url_in: SUpdateShortUrl):
        for name, value in short_url_in:
            setattr(short_url, name, value)
        self.save()
        return short_url

    def partial_update(self, short_url: ShortUrl, short_url_in: SUpdatePathShortUrl):
        for name, value in short_url_in.model_dump(
            exclude_none=True, exclude_unset=True
        ).items():
            setattr(short_url, name, value)
        self.save()
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
        self.save()
        return short_url


try:
    storage = ShortUrlsStorage.from_statement()
    logger.warning("ShortUrlsStorage loaded")
except ValidationError as e:
    storage = ShortUrlsStorage()
    storage.save()
    logger.warning("ShortUrlsStorage reloaded")
