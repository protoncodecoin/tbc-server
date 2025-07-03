from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import String, DateTime

from ..db.database import Base
from .user import User


class Podcast(Base):
    """
    ORM Mapped class for user account
    """

    __tablename__ = "podcasts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    running_episodes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    cover_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    video_file: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    user_id = mapped_column(ForeignKey("user_account.id"))
    creator: Mapped["User"] = relationship(back_populates="podcasts")

    def __repr__(self) -> str:
        return f"(title:{self.title!r}, running_episodes:{self.running_episodes!r},created_at:{self.created_at!r},user_id:{self.user_id!r})"
