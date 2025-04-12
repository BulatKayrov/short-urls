from fastapi import FastAPI, HTTPException, status, Depends
from starlette.responses import RedirectResponse

from schemas.short_url import ShortUrl

app = FastAPI(
    title="URL Shortener",
    version="1.0",
)

SHORT_URLS = [
    ShortUrl(target_url="https://example.com", slug="example"),
    ShortUrl(target_url="https://google.com", slug="google"),
]


async def prefetch_short_urls(slug: str):
    url: ShortUrl | None = next((url for url in SHORT_URLS if url.slug == slug), None)
    if url:
        return url
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/short-url", response_model=list[ShortUrl])
async def short_url():
    return SHORT_URLS


@app.get("/short-url/{slug}")
async def redirect_short_url(url=Depends(prefetch_short_urls)):
    return RedirectResponse(url.target_url)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", reload=True)
