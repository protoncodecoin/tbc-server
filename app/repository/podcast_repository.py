from typing import Annotated, List
from sqlalchemy.orm import Session

from fastapi import Depends


from ..db.database import engine
from ..models import Podcast
from ..models.user import User


async def get_session_db():
    with Session(engine) as session:
        yield session


class PodcastRepository:
    """For CRUD transaction of Podcast.

    Args:
        sess (Annotated[Session, Depends): Database Session Provider.
    """

    def __init__(self, sess: Annotated[Session, Depends(get_session_db)]):
        self.sess: Session = sess

    def insert_podcast(self, podcast: Podcast) -> bool:
        """
        Add new podcast item to the database.
        """
        try:
            self.sess.add(podcast)
            self.sess.commit()
        except Exception as e:
            print(e)  # TODO: add log
            return False
        return True

    def query_podcast(self, limit: int, offset: int) -> List[Podcast]:
        """
        Returns a list of Podcast objects.
        """
        query = self.sess.query(Podcast).limit(limit).offset(offset).all()
        return query

    def query_by_id(self, id: int) -> Podcast | None:
        """
        Get a Podcast object by ID.
        """
        query = self.sess.query(Podcast).filter_by(id=id).scalar()
        return query

    def update_podcast(self, data: Podcast) -> bool:
        """
        Update a Podcast object.
        """

        self.sess.add(data)
        self.sess.commit()
        return True

    def delete_podcast(self, id: int) -> bool:
        query = self.sess.query(Podcast).filter_by(id=id).scalar()
        if query is not None:
            self.sess.delete(query)
            self.sess.commit()
            return True
        return False
