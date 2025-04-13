from fastapi import HTTPException, status

from api.v1.short_url.crud import storage
from api.v1.short_url.schemas import ShortUrl


async def prefetch_short_urls(slug: str):
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
