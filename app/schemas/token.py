from pydantic import BaseModel
from .users import UserResponseSchema


class Token(BaseModel):
    """
    Validate token sent to client
    """

    access_token: str
    token_type: str
    id: int
    email: str
    username: str


class TokenData(BaseModel):
    """
    Validate token data to be sent to client
    """

    email: str | None = None
