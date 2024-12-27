from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column


class UUIDPkMixin:
    id: Mapped[UUID] = mapped_column(primary_key=True)