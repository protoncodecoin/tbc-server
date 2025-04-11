"""
Contains dependencies shared accross the projects.
"""

from typing import Annotated
from sqlalchemy.orm import Session


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import InvalidTokenError

# from .routers.users import oauth2_scheme
from .schemas.users import UserInDBSchema
from .schemas.token import TokenData
from .core.security import verify_password
from .core.jwt_token import SECRET_KEY, ALGORITHM
from .models.user import User

# from .db.database import SessionLocal
from .db.database import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


async def get_session_db():
    with Session(engine) as session:
        yield session


def get_user(session, email: str):
    """
    Get user from database
    """
    # if email in db:
    #     user_dict = db[email]
    #     return UserInDB(**user_dict)

    # user = session.execute(select(User).filter_by(email=email)).first()
    user = (
        session.query(
            # User.first_name,
            # User.last_name,
            User.username,
            User.email,
            User.hashed_password,
            User.is_active,
        )
        .filter_by(email=email)
        .first()
    )
    user = user._asdict()
    return UserInDBSchema(**user)


def decode_token(token: str) -> User:
    """
    Validates token and get user from db
    """
    user = get_user(fake_users_db, token)
    return user


def authenticate_user(session, email: str, password: str) -> UserInDBSchema:
    """
    Verify user password and return True if correct or False
    """
    user = get_user(session, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_session_db)],
) -> User:
    """
    Get currently logged in user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(session, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    """
    Returns an active user
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive User",
        )

    return current_user
