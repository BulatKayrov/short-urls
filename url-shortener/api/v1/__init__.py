from fastapi import APIRouter

from api.v1.short_url.views import router as short_url_router

router = APIRouter(prefix="/v1")
router.include_router(short_url_router)
