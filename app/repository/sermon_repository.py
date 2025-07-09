from typing import Annotated, List
from sqlalchemy.orm import Session

from fastapi import Depends


from ..db.database import engine
from ..models.sermon import Sermon
from ..schemas.sermon import UpdateSermon


async def get_session_db():
    with Session(engine) as session:
        yield session


class SermonRepository:
    def __init__(self, sess: Annotated[Session, Depends(get_session_db)]) -> None:
        self.sess = sess

    def insert_sermon(self, sermon: Sermon) -> bool:
        """
        Add sermon to the database.
        """
        try:
            self.sess.add(sermon)
            self.sess.commit()
        except Exception as e:
            print(e)  # TODO: add log
            return False
        return True

    def query_sermon(self, id: int) -> Sermon | None:
        """
        Return a sermon with the given id.
        """

        query = self.sess.query(Sermon).filter_by(id=id).first()

        return query

    def query_sermons(self, limit=None, offset=None) -> List[Sermon]:
        """
        Return a list of sermon objects.
        """

        query = self.sess.query(Sermon).limit(limit).offset(offset).all()
        return query

    def delete_sermon(self, id: int) -> bool | None:
        """
        Delete sermon with the given Id
        """

        query = self.sess.query(Sermon).filter_by(id=id).scalar()
        if query is None:
            return None

        if query:
            self.sess.delete(query)
            self.sess.commit()
            return True

        return False

    def update_sermon(self, id: int, sermon: UpdateSermon) -> bool:
        """
        Update a given sermon in the db.
        """
        query = self.sess.query(Sermon).filter_by(id=id).scalar()
        if query is None:
            return None

        if query:
            query.theme = sermon.theme
            query.minister = sermon.minister
            query.short_note = sermon.short_note
            query.cover_image = sermon.cover_image
            query.cld_image_public_id = sermon.cld_image_public_id
            query.audio_file = sermon.audio_file
            query.cld_audio_public_id = sermon.cld_audio_public_id

            self.sess.add(query)
            self.sess.commit()
            return True

        return True
