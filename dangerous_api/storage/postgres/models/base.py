from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase

TZ = DateTime(timezone=True)


class Base(DeclarativeBase): ...
