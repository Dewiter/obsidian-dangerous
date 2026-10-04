import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dangerous_api.storage.postgres.models.base import TZ, Base

if TYPE_CHECKING:
    from dangerous_api.storage.postgres.models.user import UserRow


class FrontierAccountRow(Base):
    __tablename__ = "frontier_accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    frontier_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    access_token: Mapped[str]
    refresh_token: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(TZ)

    user: Mapped[UserRow] = relationship("UserRow", back_populates="frontier")
