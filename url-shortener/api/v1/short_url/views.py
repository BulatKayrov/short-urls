from fastapi import APIRouter, Depends
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
