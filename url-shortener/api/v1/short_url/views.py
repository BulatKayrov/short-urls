from fastapi import APIRouter, Depends, status

from api.v1.short_url.dependencies import (
    api_or_basic,
    prefetch_short_urls,
    storage,
)
from api.v1.short_url.schemas import (
    SCreateShortUrl,
    SUpdatePathShortUrl,
    SUpdateShortUrl,
    ShortUrl,
)
from tools import RESPONSES

router = APIRouter(
    prefix="/shortener",
    tags=["Short URLs"],
    dependencies=[
        # Depends(save_storage_state),
        # Depends(user_basic_auth_required),
        # Depends(api_token_require),
        Depends(api_or_basic),
    ],
)


@router.get("/short-url", response_model=list[ShortUrl])
def short_url():
    return storage.get()


@router.get("/short-url/{slug}")
def redirect_short_url(url=Depends(prefetch_short_urls)):
    return url


@router.post(
    path="/short-url",
    response_model=ShortUrl,
    status_code=status.HTTP_201_CREATED,
    summary="Create new short url",
    description="Create a new short url",
    # dependencies=[Depends(user_basic_auth_required)],
)
def create_short_url(data: SCreateShortUrl):
    return storage.create(data)


@router.delete(
    "/short-url/{slug}", status_code=status.HTTP_204_NO_CONTENT, responses={**RESPONSES}
)
def delete_short_url(url=Depends(prefetch_short_urls)):
    return storage.delete_by_slug(slug=url.slug)


@router.put(path="/short-url/{slug}")
def update_short_url(short_in: SUpdateShortUrl, short=Depends(prefetch_short_urls)):
    return storage.update_short(short_url=short, short_url_in=short_in)


@router.patch(path="/short-url/{slug}", response_model=ShortUrl)
def patch_short_url(short_in: SUpdatePathShortUrl, short=Depends(prefetch_short_urls)):
    return storage.update_short(short_url=short, short_url_in=short_in, partial=True)
