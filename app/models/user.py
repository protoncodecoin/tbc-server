from typing import Optional, List, TYPE_CHECKING

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import DateTime

from ..db.database import Base

if TYPE_CHECKING:
    from .podcast import Podcast
    from .book import Book
    from .sermon import Sermon


class User(Base):
    """
    ORM Mapped class for user account
    """

    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )
    is_active: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    # relationships
    podcasts: Mapped[List["Podcast"]] = relationship(
        back_populates="creator",
        cascade="all, delete-orphan",
    )
    books: Mapped[List["Book"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan",
    )
    sermon: Mapped[List["Sermon"]] = relationship(
        back_populates="uploaded_by", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r} first_name={self.username!r} email={self.email!r})"
