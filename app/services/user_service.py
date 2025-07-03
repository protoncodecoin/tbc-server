from datetime import timedelta
from typing import Annotated, List

from fastapi import Depends, HTTPException, status, Header


from ..models.user import User
from ..repository.factory import get_user_repo
from ..repository.user_repository import UserRepository
from ..schemas.users import UserCreateSchema, UserResponseSchema
from ..core.security import get_password_hash, verify_password
from ..core.jwt_token import create_access_token, decode_access_token
from ..core.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..schemas.token import Token


class UserService:
    """
    Provides business process and algorithnms to UserRepository
    """

    def __init__(self, repo: Annotated[UserRepository, Depends(get_user_repo)]):
        self.repo = repo

    def create_user(self, user: User) -> bool:
        """
        Create a new user.
        """

        return self.repo.insert_user(user)

    def get_user_by_email(self, email: str) -> User | None:
        """
        Return the user with the given email.
        """
        return self.repo.query_user_by_email(email)

    def get_users(self) -> List[User]:
        """
        Return all users in the database.
        """

        return self.repo.query_users()

    def get_user_profile(self, header_token: str) -> User | None:
        """Returns the profile details of the user based on the header token passed

        Args:
            header_token (str): jwt bearer token.

        Returns:
            User: Details of the user..
        """

        token_data = decode_access_token(header_token)
        if token_data is not None:
            return self.repo.query_user_by_email(token_data.email)  # type: ignore

    def login_user(self, email: str, password: str) -> Token:

        user = self.repo.query_user_by_email(email)

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )

        data = user._asdict()  # convert user object into dictionary
        data.update({"access_token": access_token, "token_type": "bearer"})
        token_data = Token(**data)
        return token_data
