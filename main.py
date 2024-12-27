import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core.config import settings
from core.db.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()
app = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)





logging.basicConfig(
    # level=logging.INFO
    format=settings.logging.log_format,
)


