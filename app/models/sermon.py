from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, String, DateTime

from ..db.database import Base
from .user import User


class Sermon(Base):
    """
    ORM Mapped class for Sermon.
    """

    __tablename__ = "sermons"
    id: Mapped[int] = mapped_column(primary_key=True)
    theme: Mapped[str] = mapped_column(String(250))
    minister: Mapped[str] = mapped_column(String(70))
    short_note: Mapped[str] = mapped_column(String(300))
    cover_image: Mapped[str] = mapped_column(String)
    audio_file: Mapped[str] = mapped_column(String)

    user_id = mapped_column(ForeignKey("user_account.id"))
    uploaded_by: Mapped["User"] = relationship(back_populates="sermon")

    def __repr__(self) -> str:
        return f"Sermon(id={self.id!r}, theme={self.theme!r}, short_note={self.short_note!r})"
