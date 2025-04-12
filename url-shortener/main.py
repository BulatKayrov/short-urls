from fastapi import FastAPI

from schemas.short_url import ShortUrl

app = FastAPI(
    title="URL Shortener",
    version="1.0",
)


@app.get("/short-url")
async def short_url():
    return [
        ShortUrl(target_url='https://example.com', slug='example'),
        ShortUrl(target_url='https://google.com', slug='google'),
    ]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='main:app', host="0.0.0.0", port=8000)
