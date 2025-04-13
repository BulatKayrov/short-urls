from fastapi import HTTPException, status

from api.v1.short_url.schemas import ShortUrl

SHORT_URLS = [
    ShortUrl(target_url="https://example.com", slug="example"),
    ShortUrl(target_url="https://google.com", slug="google"),
]


async def prefetch_short_urls(slug: str):
    url: ShortUrl | None = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
