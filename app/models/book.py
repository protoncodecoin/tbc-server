from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime

from ..db.database import Base
from .user import User


class Book(Base):
    """
    ORM Mapped class for Book.
    """

    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    book_cover: Mapped[Optional[str]] = mapped_column(nullable=True)
    is_published: Mapped[bool] = mapped_column(default=False)
    uploaded_on: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    user_id = mapped_column(ForeignKey("user_account.id"))
    author: Mapped["User"] = relationship(back_populates="books")

    def __repr__(self) -> str:
        return f"Book(id={self.id!r}, name={self.title!r}, is_published={self.is_published}, user_id={self.user_id})"
