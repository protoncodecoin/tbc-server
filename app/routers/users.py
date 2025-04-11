from typing import Annotated
from datetime import timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import get_current_user, authenticate_user
from ..schemas.users import UserSchema, UserCreateSchema
from ..models.user import User
from ..schemas.token import Token
from ..core.jwt_token import create_access_token
from ..core.security import get_password_hash
from ..core.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_session_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session_db)]


def fake_hash_password(password: str):
    return "fakehashed" + password


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=UserSchema)
async def create_account(user_info: UserCreateSchema, session: SessionDep):

    if user_info.password != user_info.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not \
                match",
        )

    email_exist = session.execute(
        select(User).filter_by(email=user_info.email)
    ).scalar_one_or_none()

    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist",
        )

    user_hashed_password: str = get_password_hash(user_info.password)

    new_user = User(
        # first_name=user_info.first_name,
        # last_name=user_info.last_name,
        username=user_info.username,
        email=user_info.email,
        hashed_password=user_hashed_password,
        # TODO: change to false after verficication route is created
        is_active=True,
    )

    session.add(new_user)
    session.commit()

    return new_user


@router.get("/me")
def logged_in_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserSchema:
    return current_user


@router.get("/")
def get_all_users() -> list[UserSchema]:
    return []
