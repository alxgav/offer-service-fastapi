from fastapi import APIRouter

from core.config import settings

router = APIRouter(tags=["Offer"], prefix=settings.api.v1.offer)


@router.get("/", description="get all offer", name="get_offer")
async def get_offer():
    return {"message": "offer"}
