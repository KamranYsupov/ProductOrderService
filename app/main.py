from typing import Optional
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.responses import ORJSONResponse
from dependency_injector.wiring import Provide, inject

from app.core.config import settings
from app.core.container import Container, container
from app.api.v1 import routers
from app.db import DataBaseManager, db_manager

@asynccontextmanager
@inject
async def lifespan(
    fastapi_app: FastAPI,
):

    yield

    await db_manager.dispose()


def create_app() -> FastAPI:
    fastapi_app = FastAPI(
        title=settings.project_name,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    fastapi_app.container = container
    fastapi_app.include_router(routers.api_router, prefix=settings.api_v1_prefix)



    return fastapi_app


app = create_app()


