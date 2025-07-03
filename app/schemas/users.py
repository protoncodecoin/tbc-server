from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, EmailStr


class UserResponseSchema(BaseModel):
    """
    Schema to return the user entity
    """

    id: int
    username: str
    email: str
    is_active: bool
    # created_at: datetime
    # updatedAt: datetime


class UserInDBSchema(UserResponseSchema):
    """
    Schema to serializer and deserialize user
    """

    hashed_password: str

    class Config:
        from_attributes: bool = True


class UserCreateSchema(BaseModel):
    """
    Schema to create user
    """

    # first_name: str
    # last_name: str
    username: str
    email: EmailStr = Field(...)
    password: Annotated[str, Field(repr=False, min_length=8)]
    password2: str = Field(repr=False, min_length=8)
