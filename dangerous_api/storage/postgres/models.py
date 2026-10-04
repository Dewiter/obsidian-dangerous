import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

TZ = DateTime(timezone=True)


class Base(DeclarativeBase): ...


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


class FrontierAccountRow(Base):
    __tablename__ = "frontier_accounts"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )

    frontier_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    access_token: Mapped[str]
    refresh_token: Mapped[str]
    expires_at: Mapped[datetime] = mapped_column(TZ)

    user: Mapped[UserRow] = relationship(back_populates="frontier")
