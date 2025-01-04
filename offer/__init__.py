from fastapi import APIRouter

from core.config import settings
from offer.views.offer_view import router

offer_router = APIRouter(
    prefix=settings.api.prefix,
)

offer_router.include_router(router)
