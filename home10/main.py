from fastapi import FastAPI
from database import engine, Base
from repositories import DataRepository
from routers import router
from contextlib import asynccontextmanager
import uvicorn

app = FastAPI(title="Quiz API")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await DataRepository.create_table()
    yield

app = FastAPI(lifespan=lifespan, title="Quiz API")
app.include_router(router)

import logging

logging.basicConfig(level=logging.DEBUG)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
