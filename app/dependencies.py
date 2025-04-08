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
from .schemas.users import User, UserInDB
from .schemas.token import TokenData
from .models.user import fake_users_db
from .core.security import verify_password
from .core.jwt_token import SECRET_KEY, ALGORITHM

# from .db.database import SessionLocal
from .db.database import engine

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/users/login")


# async def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_session_db():
    with Session(engine) as session:
        yield session


def get_user(db, email: str):
    """
    Get user from database
    """
    if email in db:
        user_dict = db[email]
        return UserInDB(**user_dict)


def decode_token(token: str) -> User:
    """
    Validates token and get user from db
    """
    user = get_user(fake_users_db, token)
    return user


def authenticate_user(fake_db, email: str, password: str) -> UserInDB:
    """
    Verify user password and return True if correct or False
    """
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    """
    Get currently logged in user
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # user = decode_token(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, email=token_data.email)
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
