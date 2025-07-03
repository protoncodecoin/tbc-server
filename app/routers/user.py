from typing import Annotated, List
from datetime import timedelta

from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import get_password_hash

from ..dependencies import get_current_user, authenticate_user
from ..schemas.users import UserResponseSchema, UserCreateSchema
from ..models.user import User
from ..schemas.token import Token
from ..core.jwt_token import create_access_token
from ..core.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_session_db

from ..services.factory import get_user_service
from ..services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])


templates = Jinja2Templates(directory="templates")


SessionDep = Annotated[Session, Depends(get_session_db)]


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    handler: Annotated[UserService, Depends(get_user_service)],
) -> Token:
    """Validates client credentials returns token if validation is successful or returns an error

    Raises:
        HTTPException: Credential error

    Returns:
        Token: jwt bearer token
    """

    return handler.login_user(form_data.username, form_data.password)


@router.post("/signup", response_model=UserResponseSchema)
async def create_account(
    user_info: UserCreateSchema,
    handler: Annotated[UserService, Depends(get_user_service)],
):
    """
    Create new user account.
    """

    if user_info.password != user_info.password2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match",
        )

    email_exist = handler.get_user_by_email(user_info.email)
    if email_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exist",
        )
    user_hashed_password: str = get_password_hash(user_info.password)

    new_user = User(
        username=user_info.username,
        email=user_info.email,
        hashed_password=user_hashed_password,
        # TODO: change to false after verification route is created
        is_active=True,
    )

    new_user = handler.create_user(new_user)
    if new_user:
        return handler.get_user_by_email(user_info.email)
    raise HTTPException(
        detail="Failed to create user", status_code=status.HTTP_400_BAD_REQUEST
    )


@router.get("/me")
async def logged_in_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> UserResponseSchema:

    return current_user  # type: ignore


@router.get("/profile")
async def logged_in_user_profile(
    handler: Annotated[UserService, Depends(get_user_service)],
    x_user_token: Annotated[str, Header()],
) -> UserResponseSchema:

    query_result = handler.get_user_profile(x_user_token)
    if query_result is None:
        raise HTTPException(
            detail="User not Found", status_code=status.HTTP_404_NOT_FOUND
        )
    return query_result  # type: ignore


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(
    currrent_user: Annotated[User, Depends(get_current_user)],
    handler: Annotated[UserService, Depends(get_user_service)],
):

    return handler.get_users()


@router.get("/render/index", response_class=HTMLResponse)
async def render_home(
    request: Request, current_user: Annotated[User, Depends(get_current_user)]
):
    return templates.TemplateResponse(
        request, name="index.html", context={"user": current_user.username}
    )
