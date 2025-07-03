from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
import jwt

from ..schemas.token import TokenData
from .constants import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create and return access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    """Decodes jwt token and returns token data if valid or raise credential errors.

    Args:
        token (str): Token retrieved from the header.

    Raises:
        credentials_exception: Exception raised if the token is invalid.

    Returns:
        TokenData: Contains the email of the user.
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
    except jwt.InvalidTokenError:
        raise credentials_exception

    return token_data
