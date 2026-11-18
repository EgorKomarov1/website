from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path

from api.routing.routers import router
from api.routing.pages import pages_router
from database.db import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    engine.dispose()

app = FastAPI(title='news_api', lifespan=lifespan)

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
app.include_router(pages_router)

project_directory = Path(__file__).resolve().parents[1]
for directory in ('css', 'js', 'assets'):
    app.mount(f'/{directory}', StaticFiles(directory=project_directory / directory), name=directory)
