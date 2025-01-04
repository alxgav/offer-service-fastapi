import uuid
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.db.db_helper import db_helper
from offer.schemas.offer import ReadOffer, CreateOffer
from offer.services.services import (
    get_offers,
    get_offer,
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
    offer_id: Annotated[
        uuid.UUID, Query(..., description="The UUID of the offer to get")
    ],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        offer = await get_offer(session, offer_id)
        return offer
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Offer with ID {offer_id} not found.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while getting the offer: {e}",
        )
    # return offer


@router.delete(
    "/",
    description="delete offers",
    name="delete offers",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete(
    offer_id: Annotated[
        uuid.UUID, Query(..., description="The UUID of the offer to delete")
    ],
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        await delete_offer(session, offer_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the offer.",
        )


@router.patch(
    "/",
    description="update offer",
    name="update offer",
    response_model=ReadOffer,
    response_model_exclude_none=True,
    status_code=status.HTTP_200_OK,
)
async def update(
    offer_id: Annotated[
        uuid.UUID, Query(..., description="The UUID of the offer to update")
    ],
    offer_update: CreateOffer,
    session: Annotated[AsyncSession, Depends(db_helper.session_getter)],
):
    try:
        offer = await update_offer(session, offer_id, offer_update)
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
