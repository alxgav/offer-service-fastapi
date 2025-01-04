from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from offer.schemas.offer_options import CreateOfferOptions, ReadOfferOptions


class Offer(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None


class CreateOffer(Offer):
    offer_option: Optional[CreateOfferOptions] = None


class ReadOffer(Offer):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: UUID
    offer_option: Optional[ReadOfferOptions] = None
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
