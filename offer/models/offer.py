import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.db.base import Base
from core.db.mixins.create_at_mixin import CreatedAtMixin
from core.db.mixins.id_mixin import UUIDPkMixin
from offer.models.mixins.OfferRelationMixin import OfferRelationMixin


class Offer(UUIDPkMixin, CreatedAtMixin, Base):

    __table_args__ = {"schema": "offer", "extend_existing": True}

    title: Mapped[str]
    image: Mapped[str]
    description: Mapped[str]
    offer_option: Mapped["OfferOption"] = relationship(
        "OfferOption",
        back_populates="offer",
        uselist=False,
        cascade="all, delete-orphan",
    )
    offer_location: Mapped["OfferLocationDetail"] = relationship(
        "OfferLocationDetail",
        back_populates="offer",
        uselist=False,
        cascade="all, delete-orphan",
    )

    price_details: Mapped[list["OfferPriceDetails"]] = relationship(
        "OfferPriceDetails", back_populates="offer", cascade="all, delete-orphan"
    )
    type: Mapped[list["OfferType"]] = relationship(
        "OfferType", back_populates="offers", cascade="all, delete-orphan"
    )
    requests: Mapped[list["OfferRequest"]] = relationship(
        "OfferRequest", back_populates="offer", cascade="all, delete-orphan"
    )
    ratings: Mapped[list["OfferRating"]] = relationship(
        "OfferRating", back_populates="offer", cascade="all, delete-orphan"
    )


class OfferPriceDetails(UUIDPkMixin, OfferRelationMixin, Base):
    _offer_back_populates = "price_details"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id))
    caption: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    image: Mapped[str]
    # offer: Mapped[Offer] = relationship("Offer", back_populates="price_details")


#
#
class OfferOption(UUIDPkMixin, OfferRelationMixin, Base):
    _offer_back_populates = "offer_option"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id))
    is_temporary: Mapped[bool]
    temporary_to: Mapped[datetime] = mapped_column(default=func.now())


class OfferLocationDetail(UUIDPkMixin, OfferRelationMixin, Base):
    _offer_back_populates = "offer_location"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id))

    location_text: Mapped[str]
    lat: Mapped[float] = mapped_column(default=0.0)
    lng: Mapped[float] = mapped_column(default=0.0)
    street_name: Mapped[str] = mapped_column(default="")
    house_number: Mapped[str] = mapped_column(default="")
    zip_code: Mapped[int]
    city: Mapped[str] = mapped_column(default="")
    country: Mapped[str] = mapped_column(default="")
    federal_state: Mapped[str] = mapped_column(default="")
    radius: Mapped[int] = mapped_column(default=0)


class OfferType(UUIDPkMixin, CreatedAtMixin, OfferRelationMixin, Base):
    _offer_back_populates = "type"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id))
    name: Mapped[str]
    description: Mapped[str]
    # offer: Mapped[Offer] = relationship("Offer", back_populates="type")


#
#
class OfferRequest(UUIDPkMixin, OfferRelationMixin, Base):
    _offer_back_populates = "requests"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id))
    # offer: Mapped[Offer] = relationship("Offer", back_populates="requests")
    request_made_at: Mapped[datetime]
    request_made_by: Mapped[str]
    price_detail_id: Mapped[int]
    request_status: Mapped[int]


class OfferRating(UUIDPkMixin, CreatedAtMixin, OfferRelationMixin, Base):
    _offer_back_populates = "ratings"
    offer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey(Offer.id))
    # offer: Mapped[Offer] = relationship("Offer", back_populates="ratings")
    caption: Mapped[str]
    description: Mapped[str]
    rating: Mapped[float] = mapped_column(default=0.0, nullable=False)
