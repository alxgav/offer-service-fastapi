from fastapi import APIRouter

from core.config import settings
from offer.view import router

offer_router = APIRouter(
    prefix=settings.api.prefix,
)

offer_router.include_router(router)
