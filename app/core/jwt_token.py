from datetime import datetime, timedelta, timezone

import jwt
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
