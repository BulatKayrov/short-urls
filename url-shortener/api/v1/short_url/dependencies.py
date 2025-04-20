from logging import getLogger

from fastapi import HTTPException, status, BackgroundTasks, Request

from api.v1.short_url.crud import storage
from api.v1.short_url.schemas import ShortUrl

logger = getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})


def prefetch_short_urls(slug: str):
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def save_storage_state(bg_task: BackgroundTasks, request: Request):
    logger.info(request.method)
    yield
    if request.method not in UNSAFE_METHODS:
        logger.info("Saving storage state")
        bg_task.add_task(storage.save())
