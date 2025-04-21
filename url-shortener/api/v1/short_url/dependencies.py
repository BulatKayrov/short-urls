from logging import getLogger

from fastapi import HTTPException, status, BackgroundTasks, Request
from fastapi.params import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)

from api.v1.short_url.crud import storage
from api.v1.short_url.schemas import ShortUrl
from core.config import settings

logger = getLogger(__name__)

UNSAFE_METHODS = frozenset({"POST", "PUT", "PATCH", "DELETE"})

static_api_token = HTTPBearer(
    auto_error=False,
    scheme_name="Static API token",
    description="Static API token",
)

_user_basic_http_auth = HTTPBasic(
    scheme_name="Basic",
    description="Basic auth scheme, username + password",
    auto_error=False,
)


def user_basic_auth_required(
    request: Request,
    credentials: HTTPBasicCredentials | None = Depends(_user_basic_http_auth),
):
    if request.method not in UNSAFE_METHODS:
        return
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials [username or password]",
            headers={"WWW-Authenticate": "Basic"},
        )
    return validate_basic_auth(credentials=credentials)


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
        bg_task.add_task(storage.save)


def api_token_require(
    request: Request,
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
):
    if request.method not in UNSAFE_METHODS:
        return
    logger.info("api token required %s", api_token)
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token is required.",
        )
    return validate_api_token(api_token=api_token)


def validate_api_token(api_token: HTTPAuthorizationCredentials):
    if api_token.credentials not in settings.API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token"
        )
    return api_token


def validate_basic_auth(credentials: HTTPBasicCredentials):
    if (
        credentials.username in settings.USER_DB
        and settings.USER_DB[credentials.username] == credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password]",
        headers={"WWW-Authenticate": "Basic"},
    )


def api_or_basic(
    request: Request,
    api_token: HTTPAuthorizationCredentials | None = Depends(static_api_token),
    credentials: HTTPBasicCredentials | None = Depends(_user_basic_http_auth),
):
    if request.method not in UNSAFE_METHODS:
        return

    if api_token:
        return validate_api_token(api_token)
    if credentials:
        return validate_basic_auth(credentials=credentials)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token is required or username and password is required.",
    )
