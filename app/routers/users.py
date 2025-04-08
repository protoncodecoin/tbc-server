from typing import Annotated
from datetime import timedelta

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..dependencies import get_current_user, authenticate_user
from ..schemas.users import UserInDB, User
from ..models.user import fake_users_db
from ..schemas.token import Token
from ..core.jwt_token import create_access_token
from ..core.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_session_db

router = APIRouter(prefix="/api/v1/users", tags=["users"])

SessionDep = Annotated[Session, Depends(get_session_db)]


def fake_hash_password(password: str):
    return "fakehashed" + password


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
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


@router.get("/me")
def logged_in_user(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user


@router.get("/")
def get_all_users() -> list[User]:
    return []


@router.get("/{id}")
def get_user(id: int, token: Annotated[str, Depends(get_current_user)]) -> User:
    return {"name": "Prince", "path_param": id, "token": token}


@router.put("/{id}")
def update_user(id: int) -> User:
    return {"msg": "Credentials updated", "path_param": id}
