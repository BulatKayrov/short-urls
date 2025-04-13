from fastapi import FastAPI

from api import router

app = FastAPI(title="Сокращатель ссылок", version="1.0")
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="main:app", reload=True)
