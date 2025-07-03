from typing import List, Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select

from fastapi import Depends

from ..models.user import User
from ..db.database import engine


async def get_session_db():
    with Session(engine) as session:
        yield session


class UserRepository:

    def __init__(self, sess: Annotated[Session, Depends(get_session_db)]):
        """
        For CRUD transaction of the user.
        """
        self.sess: Session = sess

    def insert_user(self, user: User) -> bool:
        try:
            self.sess.add(user)
            self.sess.commit()
        except Exception as e:
            # TODO: add a logger to log exeception
            print(e)
            return False
        return True

    def query_users(self) -> List[User]:
        query = self.sess.scalars(select(User)).all()

        return query

    def query_user_by_email(self, email: str) -> User | None:
        """
        Get a user by using the provided email. Returns none if no user is found
        """
        query = (
            self.sess.query(
                User.id,
                User.username,
                User.email,
                User.hashed_password,
                User.is_active,
            )
            .filter_by(email=email)
            .first()
        )

        return query
