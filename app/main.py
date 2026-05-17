from contextlib import asynccontextmanager

import swisseph as swe
from fastapi import FastAPI

from app.config import get_settings
from app.routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    swe.set_ephe_path(settings.EPHE_PATH)
    yield
    swe.close()


app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
)

app.include_router(router=router)
