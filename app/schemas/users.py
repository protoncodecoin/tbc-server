from pydantic import BaseModel


class User(BaseModel):
    """
    Model the user entity
    """

    first_name: str
    last_name: str
    email: str
    is_active: bool


class UserInDB(User):
    """
    Serializer and deserialize user
    """

    hashed_password: str
