from logging import getLogger

from fastapi import HTTPException, status, BackgroundTasks, Request
from fastapi.params import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.v1.short_url.crud import storage
from api.v1.short_url.schemas import ShortUrl
from core.config import settings

logger = getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

static_api_token = HTTPBearer(
    auto_error=False, scheme_name="Static API token", description="Static API token"
)


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


def api_token_require(
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
):
    logger.info("api token required %s", api_token)
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )

    if api_token.credentials not in settings.API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )
    return api_token
