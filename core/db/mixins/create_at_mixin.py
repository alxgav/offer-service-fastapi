from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column


class CreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(onupdate=func.now(), nullable=True)
    # created_by: Mapped[str] = mapped_column(nullable=False)
    # updated_by: Mapped[str] = mapped_column(nullable=True)
