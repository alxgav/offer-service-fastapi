import logging
import uuid
from typing import Sequence

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from offer.models.offer import Offer, OfferOption, OfferLocationDetail
from offer.schemas.offer import CreateOffer

logger = logging.getLogger(__name__)


async def create_offer(session: AsyncSession, offer_data: CreateOffer):

    offer_dict = offer_data.model_dump(exclude={"offer_option", "offer_location"})
    offer_option_dict = (
        offer_data.offer_option.model_dump() if offer_data.offer_option else None
    )
    offer_location_dict = (
        offer_data.offer_location.model_dump() if offer_data.offer_location else None
    )

    offer = Offer(**offer_dict)

    if offer_option_dict:
        offer.offer_option = OfferOption(**offer_option_dict)

    if offer_location_dict:
        offer.offer_location = OfferLocationDetail(**offer_location_dict)

    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return offer


async def get_offers(session: AsyncSession) -> Sequence[Offer]:
    stmt = select(Offer).options(
        selectinload(Offer.offer_option), selectinload(Offer.offer_location)
    )
    result = await session.execute(stmt)
    offers = result.scalars().all()
    return [offer for offer in offers]


async def delete_offer(offer: Offer, session: AsyncSession) -> None:
    try:
        await session.delete(offer)
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the offer: {str(e)}",
        )


async def update_offer(
    offer: Offer, session: AsyncSession, offer_update: CreateOffer
) -> Offer:

    if offer:
        offer_dict = offer_update.model_dump(exclude={"offer_option"})
        for key, value in offer_dict.items():
            setattr(offer, key, value)

        if offer.offer_option:
            if offer_update.offer_option:
                offer_option_data = offer_update.offer_option.model_dump()
                for key, value in offer_option_data.items():
                    setattr(offer.offer_option, key, value)
            else:
                offer.offer_option = None
        elif offer_update.offer_option:
            offer.offer_option = OfferOption(**offer_update.offer_option.model_dump())
        if offer.offer_location:
            if offer_update.offer_location:
                offer_location_data = offer_update.offer_location.model_dump()
                for key, value in offer_location_data.items():
                    setattr(offer.offer_location, key, value)
            else:
                offer.offer_location = None
        elif offer_update.offer_location:
            offer.offer_location = OfferLocationDetail(
                **offer_update.offer_location.model_dump()
            )
    else:
        raise ValueError(f"Offer with ID {offer.id} not found.")
    await session.commit()
    await session.refresh(offer)
    return offer
