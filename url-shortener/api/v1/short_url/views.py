from fastapi import APIRouter, Depends, status

from api.tools import RESPONSES
from api.v1.short_url.dependencies import storage, prefetch_short_urls
from api.v1.short_url.schemas import ShortUrl, SCreateShortUrl, SUpdateShortUrl

router = APIRouter(prefix="/shortener", tags=["Short URLs"])


@router.get("/short-url", response_model=list[ShortUrl])
async def short_url():
    return storage.get()


@router.get("/short-url/{slug}")
async def redirect_short_url(url=Depends(prefetch_short_urls)):
    return url
    # return RedirectResponse(url.target_url)


@router.post(
    path="/short-url",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
    summary="Create new short url",
    description="Create a new short url",
)
async def create_short_url(data: SCreateShortUrl):
    return storage.create(data=data)


@router.delete(
    "/short-url/{slug}", status_code=status.HTTP_204_NO_CONTENT, responses={**RESPONSES}
)
async def delete_short_url(url=Depends(prefetch_short_urls)):
    return storage.delete_by_slug(slug=url.slug)


@router.put(path="/short-url/{slug}")
async def update_short_url(
    short_in: SUpdateShortUrl, short=Depends(prefetch_short_urls)
):
    return storage.update_by_slug(short_url=short, short_url_in=short_in)
