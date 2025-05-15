import logging

from fastapi import FastAPI
from starlette.responses import RedirectResponse

from api import router
from app_lifespan import lifespan
from core.config import settings

app = FastAPI(title="Сокращатель ссылок", version="1.0", lifespan=lifespan)
app.include_router(router)

logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)


@app.get("/")
def root():
    return RedirectResponse(url="http://0.0.0.0:8000/docs")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
