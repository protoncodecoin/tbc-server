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

    def update_podcast(self, id: int, data: Podcast) -> bool:
        """
        Update a Podcast object.
        """
        query = self.sess.query(Podcast).filter_by(id=id).scalar()
        if query is not None:
            query.title = data.title
            query.running_episodes = data.running_episodes
            query.user_id = data.user_id
            query.cover_image = data.cover_image
            query.cld_image_public_id = data.cld_image_public_id
            query.cld_video_public_id = data.cld_video_public_id
            query.video_file = data.video_file

            self.sess.add(query)
            self.sess.commit()
            return True
        return False

    def delete_podcast(self, id: int) -> bool:
        query = self.sess.query(Podcast).filter_by(id=id).scalar()
        if query is not None:
            self.sess.delete(query)
            self.sess.commit()
            return True
        return False
