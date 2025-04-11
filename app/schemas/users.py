from pydantic import BaseModel


class UserSchema(BaseModel):
    """
    Schema to model the user entity
    """

    # first_name: str
    # last_name: str
    username: str
    email: str
    is_active: bool


class UserInDBSchema(UserSchema):
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
    email: str
    password: str
    password2: str
