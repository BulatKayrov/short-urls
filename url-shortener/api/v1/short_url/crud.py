from fastapi import HTTPException
from pydantic import BaseModel

from api.v1.short_url.schemas import ShortUrl, SCreateShortUrl

SHORT_URLS = [
    ShortUrl(target_url="https://example.com", slug="example"),
    ShortUrl(target_url="https://google.com", slug="google"),
]


class ShortUrlsStorage(BaseModel):
    slug_to_short_url: dict[str, ShortUrl] = {}

    def get(self):
        return list(self.slug_to_short_url.values())

    def get_by_slug(self, slug):
        return self.slug_to_short_url.get(slug)

    def create(self, data: SCreateShortUrl):
        short_url = ShortUrl(**data.model_dump())
        if short_url.slug in self.slug_to_short_url:
            raise HTTPException(status_code=400, detail="Slug already exists")
        self.slug_to_short_url[short_url.slug] = short_url
        return short_url

    def delete_by_slug(self, slug):
        if slug not in self.slug_to_short_url:
            raise HTTPException(status_code=404, detail="Slug not found")
        self.slug_to_short_url.pop(slug, None)
        return

    def delete_short_url(self, short_url: ShortUrl):
        self.delete_by_slug(slug=short_url.slug)


storage = ShortUrlsStorage()

for obj in SHORT_URLS:
    storage.create(data=SCreateShortUrl(**obj.model_dump()))
