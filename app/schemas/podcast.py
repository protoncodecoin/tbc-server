from typing import Optional
from pydantic import BaseModel, Field

from ..schemas.users import UserResponseSchema

from ..models.user import User


class CreatePodcast(BaseModel):
    title: str = Field(..., description="Title of the Podcast Content you are creating")
    running_episodes: int = Field(..., ge=1)
    user_id: Optional[int] = None
    cover_image: str
    cld_image_public_id: str
    cld_video_public_id: str
    video_file: str


class PodcastResponse(CreatePodcast):
    # user_id: int
    # creator: UserSchema
    pass


class UpdatePodcast(CreatePodcast):
    pass


class PartialUpdatePodcast(BaseModel):
    title: Optional[str] = Field(
        description="Title of the Podcast Content you are creating", default=None
    )
    running_episodes: Optional[int] = Field(default=None, ge=1)
