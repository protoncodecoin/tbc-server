from pydantic import BaseModel


class Token(BaseModel):
    """
    Validate token sent to client
    """

    access_token: str
    token_type: str


class TokenData(Token):
    """
    Validate token data to be sent to client
    """

    email: str | None = None
