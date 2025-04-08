from typing import Optional

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Uuid, DateTime


class Base(DeclarativeBase):
    pass


class User(Base):
    """
    ORM Mapped class for user account
    """

    __tablename__ = "user_account"

    id: Mapped[Uuid] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30))
    last_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str]
    hashed_password: Mapped[str]
    created_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool]

    def __repr__(self) -> str:
        return f"User(id={self.id!r} first_name={self.first_name!r} last_name={self.last_name!r} email={self.email!r})"


fake_users_db = {
    "johndoe@example.com": {
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": False,
    },
    "alice@example.com": {
        "first_name": "Alice",
        "last_name": "Wonderson",
        "email": "alice@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "is_active": True,
    },
}
