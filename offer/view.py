from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=["Offer"], prefix=settings.api.v1.offer)


@router.get("/")
async def get_offer():
    return {"message": "offer"}
