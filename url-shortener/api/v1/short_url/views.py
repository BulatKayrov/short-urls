from typing import Annotated

from fastapi import APIRouter, Depends, status, Form
from pydantic import AnyHttpUrl
from starlette.responses import RedirectResponse

from api.v1.short_url.dependencies import SHORT_URLS, prefetch_short_urls
from api.v1.short_url.schemas import ShortUrl

router = APIRouter(prefix="/shortener", tags=["Short URLs"])


@router.get("/short-url", response_model=list[ShortUrl])
async def short_url():
    return SHORT_URLS


@router.get("/short-url/{slug}")
async def redirect_short_url(url=Depends(prefetch_short_urls)):
    return RedirectResponse(url.target_url)


@router.post(
    path="/short-url",
    # response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
    summary="Create new short url",
    description="Create a new short url",
)
async def create_short_url(
    target_url: Annotated[AnyHttpUrl, Form()],
    slug: Annotated[str, Form(min_length=5, max_length=100)],
):
    return {"data": ShortUrl(target_url=target_url, slug=slug), "status": 201}
