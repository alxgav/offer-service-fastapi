import uuid

from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.db.db_helper import db_helper
from offer.models.offer import Offer


async def get_offer_by_id(
    offer_id: uuid.UUID, session: AsyncSession = Depends(db_helper.session_getter)
) -> Offer:
    stmt = (
        select(Offer)
        .where(Offer.id == offer_id)
        .options(selectinload(Offer.offer_option), selectinload(Offer.offer_location))
    )
    result = await session.execute(stmt)
    offer = result.scalars().first()
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer id {offer_id} not found",
        )
    return offer
