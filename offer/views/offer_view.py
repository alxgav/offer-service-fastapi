import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db.db_helper import db_helper
from offer.models.offer import Offer
from offer.schemas.offer import ReadOffer, CreateOffer
from offer.services.dependencies import get_offer_by_id

from offer.services.services import (
    get_offers,
    create_offer,
    delete_offer,
    update_offer,
)

router = APIRouter(tags=["Offer"], prefix=settings.api.v1.offer)


@router.post(
    "/",
    description="post offer",
    name="create offer",
    # response_model=ReadOffer,
    status_code=status.HTTP_201_CREATED,
    response_model_exclude_none=True,
)
async def create(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    offer_create: CreateOffer,
):
    try:
        offer = await create_offer(session=session, offer_data=offer_create)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while getting offers: {e}",
        )

    return offer


@router.get(
    "/offers/",
    description="get offers",
    name="get offers",
    response_model=list[ReadOffer],
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_all_offers(
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    try:
        offers = await get_offers(session=session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while getting offers: {e}",
        )
    return offers


@router.get(
    "/",
    description="get offer",
    name="get offer",
    response_model=ReadOffer,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def get_offer_by_id(
    offer_id: Annotated[uuid.UUID, Query(..., description="Offer ID")],
    offer: Annotated[Offer, Depends(get_offer_by_id)],
):
    return offer


@router.delete(
    "/",
    description="delete offer",
    name="delete offer",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    offer_id: Annotated[uuid.UUID, Query(..., description="Offer ID")],
    offer: Annotated[Offer, Depends(get_offer_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        await delete_offer(offer=offer, session=session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while getting offers: {e}",
        )
    return


@router.patch(
    "/",
    description="update offer",
    name="update offer",
    response_model=ReadOffer,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def update(
    offer_id: Annotated[uuid.UUID, Query(..., description="Offer ID")],
    offer: Annotated[Offer, Depends(get_offer_by_id)],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
    offer_update: CreateOffer,
):
    try:
        offer = await update_offer(
            offer=offer, session=session, offer_update=offer_update
        )
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the offer: {e}",
        )
    return offer
