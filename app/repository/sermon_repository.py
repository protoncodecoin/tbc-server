from typing import Annotated, List
from sqlalchemy.orm import Session

from fastapi import Depends


from ..db.database import engine
from ..models.sermon import Sermon


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

    def query_sermons(self, limit=None, offset=None) -> List[Sermon]:
        """
        Return a list of sermon objects.
        """

        query = self.sess.query(Sermon).limit(limit).offset(offset).all()
        return query
