from core.db.base import Base
from core.db.mixins.id_mixin import UUIDPkMixin


class Offer(UUIDPkMixin, Base):

    title: str
    description: str