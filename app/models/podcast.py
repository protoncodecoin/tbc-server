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
    podcast_title: Mapped[str] = mapped_column(String(100), nullable=False)
    running_episodes: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    cover_image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cld_image_public_id: Mapped[Optional[str]] = mapped_column(String)

    user_id = mapped_column(ForeignKey("user_account.id"))

    # relationship
    creator: Mapped["User"] = relationship(back_populates="podcasts")
    podcast_episodes: Mapped[list["PodcastEpisode"]] = relationship(
        back_populates="podcasts"
    )

    def __repr__(self) -> str:
        return f"(title:{self.podcast_title!r}, running_episodes:{self.running_episodes!r},created_at:{self.created_at!r},user_id:{self.user_id!r})"


class PodcastEpisode(Base):
    __tablename__ = "podcast_episodes"
    id: Mapped[int] = mapped_column(primary_key=True)
    episode_title: Mapped[str] = mapped_column(String(100), nullable=False)
    episode_number: Mapped[int] = mapped_column()
    video_file: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    cld_video_public_id: Mapped[Optional[str]] = mapped_column(String)
    podcast_id = mapped_column(ForeignKey("podcasts.id"))

    # relationship
    podcasts: Mapped["Podcast"] = relationship(back_populates="podcast_episodes")

    def __repr__(self) -> str:
        return f"(episode_title: {self.episode_title!r}, episode_number: {self.episode_number!r})"
