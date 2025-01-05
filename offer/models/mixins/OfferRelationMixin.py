from sqlalchemy.orm import declared_attr, Mapped, relationship


class OfferRelationMixin:
    _offer_back_populates: str | None = None

    @declared_attr
    def offer(cls) -> Mapped["Offer"]:
        return relationship(
            "Offer",
            back_populates=cls._offer_back_populates,
        )
