from datetime import datetime
from random import random
from typing import Optional
from uuid import UUID

from faker import Faker
from pydantic import BaseModel, ConfigDict, Field

from offer.schemas.offer_locations import CreateOfferLocations, ReadOfferLocations
from offer.schemas.offer_options import CreateOfferOptions, ReadOfferOptions

fake = Faker()


class Offer(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None


class CreateOffer(Offer):
    offer_option: Optional[CreateOfferOptions] = None
    offer_location: Optional[CreateOfferLocations] = None
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": fake.sentence(nb_words=4),
                "image": fake.image_url(),
                "description": fake.text(max_nb_chars=200),
                "offer_option": {"is_temporary": fake.boolean()},
                "offer_location": {
                    "location_text": fake.city(),
                    "lat": fake.latitude(),
                    "lng": fake.longitude(),
                    "street_name": fake.street_name(),
                    "house_number": fake.building_number(),
                    "zip_code": fake.zipcode(),
                    "city": fake.city(),
                    "country": fake.country(),
                    "federal_state": fake.state(),
                    "radius": fake.random_int(min=0, max=100),
                },
            }
        }
    }


class ReadOffer(Offer):
    model_config = ConfigDict(
        from_attributes=True,
    )
    id: UUID
    offer_option: Optional[ReadOfferOptions] = None
    offer_location: Optional[ReadOfferLocations] = None
    created_at: datetime
    updated_at: Optional[datetime] = Field(default=None)
