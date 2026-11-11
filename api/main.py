from fastapi import FastAPI
from database.db import engine
from contextlib import asynccontextmanager

from database.db import engine
from api.routing.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    engine.dispose()

app = FastAPI(title='news_api')

app.include_router(router)