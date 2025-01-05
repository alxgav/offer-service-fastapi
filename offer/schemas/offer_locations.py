from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class OfferLocations(BaseModel):
    location_text: str
    lat: float = Field(default=0.0)
    lng: float = Field(default=0.0)
    street_name: str = Field(default="")
    house_number: str = Field(default="")
    zip_code: int
    city: str = Field(default="")
    country: str = Field(default="")
    federal_state: str = Field(default="")
    radius: int = Field(default=0)


class CreateOfferLocations(OfferLocations):
    pass


class ReadOfferLocations(OfferLocations):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: UUID
