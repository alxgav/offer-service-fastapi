from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class OfferOptions(BaseModel):
    is_temporary: bool = True


class CreateOfferOptions(OfferOptions):
    pass


class ReadOfferOptions(OfferOptions):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: UUID
    temporary_to: Optional[datetime] = None
