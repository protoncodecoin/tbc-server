from typing import Optional
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator

from ..core.constants import AUDIO_FILE_TYPES, IMAGE_FILE_TYPES


class CreateSermon(BaseModel):
    """
    Pydantic Model to create Sermon.
    """

    theme: str = Field(..., max_length=250)
    minister: str = Field(..., max_length=70)
    short_note: str = Field(..., max_length=300)
    cover_image: str
    audio_file: str
    user_id: Optional[int] = Field(default=None)

    @model_validator(mode="after")
    def validate_cover_image(self) -> Self:
        cover_img_ext = self.cover_image.split(".")[-1]
        audio_file = self.audio_file.split(".")[-1]
        if not cover_img_ext in IMAGE_FILE_TYPES:
            raise ValueError("Image type not supported")
        if not audio_file in AUDIO_FILE_TYPES:
            raise ValueError("Audio type not supported")
        if self.user_id is None:
            raise ValueError("User Field cannot be empty")
        return self


class ResponseSermon(BaseModel):
    """
    Pydantic Model Response for Sermon
    """

    theme: str
    minister: str
    short_note: str
    cover_image: str
    audio_file: str
    user_id: int
