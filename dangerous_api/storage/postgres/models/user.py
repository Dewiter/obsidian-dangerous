import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dangerous_api.storage.postgres.models.base import TZ, Base

if TYPE_CHECKING:
    from dangerous_api.storage.postgres.models.frontier import (
        FrontierAccountRow,
    )


class UserRow(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password_hash: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TZ, server_default=func.now())

    frontier: Mapped[FrontierAccountRow | None] = relationship(
        "FrontierAccountRow",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )
