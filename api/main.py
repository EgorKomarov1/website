from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import engine
from contextlib import asynccontextmanager

from database.db import engine
from api.routing.routers import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    engine.dispose()

app = FastAPI(title='news_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:63342',
        'http://127.0.0.1:63342',
    ],
    allow_credentials=False,
    allow_methods=['GET'],
    allow_headers=['*'],
)

app.include_router(router)
