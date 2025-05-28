from logging import getLogger
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
)

from api.v1.short_url.auth.service import redis_auth_helper, redis_tokens_helper
from api.v1.short_url.crud import storage
from api.v1.short_url.schemas import ShortUrl

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
    credentials: HTTPBasicCredentials = Depends(_user_basic_http_auth),
):
    if request.method not in UNSAFE_METHODS:
        return
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials [username or password]",
            headers={"WWW-Authenticate": "Basic"},
        )
    validate_basic_auth(credentials=credentials)


def prefetch_short_urls(slug: str):
    url: ShortUrl | None = storage.get_by_slug(slug=slug)
    if url:
        return url
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


def api_token_require(
    request: Request,
    api_token: Annotated[HTTPAuthorizationCredentials, Depends(static_api_token)],
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
    if redis_tokens_helper.token_exists(api_token.credentials):
        return api_token
    print(api_token.credentials)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API token (HTTPAuthorizationCredentials)",
    )


def validate_basic_auth(credentials: HTTPBasicCredentials):

    if redis_auth_helper.validate_user_password(
        username=credentials.username, password=credentials.password
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials [username or password] (HTTPBasicCredentials)",
        headers={"WWW-Authenticate": "Basic"},
    )


def api_or_basic(
    request: Request,
    api_token: Annotated[HTTPAuthorizationCredentials, Depends(static_api_token)],
    credentials: Annotated[HTTPBasicCredentials, Depends(_user_basic_http_auth)],
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
