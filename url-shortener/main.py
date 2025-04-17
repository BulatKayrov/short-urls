import logging

from fastapi import FastAPI

from api import router
from app_lifespan import lifespan
from core.config import settings

app = FastAPI(title="Сокращатель ссылок", version="1.0", lifespan=lifespan)
app.include_router(router)

logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", reload=True)
