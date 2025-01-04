import logging
import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from offer.models.offer import Offer, OfferOption
from offer.schemas.offer import CreateOffer

logger = logging.getLogger(__name__)


async def create_offer(session: AsyncSession, offer_data: CreateOffer):
    # Extract data using model_dump()
    offer_dict = offer_data.model_dump(exclude={"offer_option"})
    offer_option_dict = (
        offer_data.offer_option.model_dump() if offer_data.offer_option else None
    )

    # Create the Offer model
    offer = Offer(**offer_dict)

    # Create the OfferOption model if applicable
    if offer_option_dict:
        offer.offer_option = OfferOption(**offer_option_dict)

    # Add and commit to the database
    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return offer


async def get_offers(session: AsyncSession) -> Sequence[Offer]:
    stmt = select(Offer).options(selectinload(Offer.offer_option))
    result = await session.execute(stmt)
    offers = result.scalars().all()
    return [offer for offer in offers]


async def delete_offer(session: AsyncSession, offer_id: uuid.UUID) -> None:
    stmt = select(Offer).where(Offer.id == offer_id)
    result = await session.execute(stmt)
    offer = result.scalars().one_or_none()
    if offer:
        await session.delete(offer)
        await session.commit()
        logger.info(f"Offer with id {offer_id} deleted successfully.")
    else:
        raise ValueError(f"Offer with ID {offer_id} not found.")


#     get offer by id
async def get_offer(session: AsyncSession, offer_id: uuid.UUID) -> Offer:
    stmt = (
        select(Offer)
        .where(Offer.id == offer_id)
        .options(selectinload(Offer.offer_option))
    )
    result = await session.execute(stmt)
    offer = result.scalars().one()
    if not offer:
        raise ValueError(f"Offer with ID {offer_id} not found.")
    return offer


#     update offer


async def update_offer(
    session: AsyncSession, offer_id: uuid.UUID, offer_update: CreateOffer
) -> Offer:
    stmt = (
        select(Offer)
        .options(selectinload(Offer.offer_option))
        .where(Offer.id == offer_id)
    )
    result = await session.execute(stmt)
    offer = result.scalars().one()
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
    else:
        raise ValueError(f"Offer with ID {offer_id} not found.")
    await session.commit()
    await session.refresh(offer)
    return offer
