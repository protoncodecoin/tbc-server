"""
Provides a loose coupling design between the api endpoints and the service layer.
"""

from typing import Annotated

from fastapi import Depends

from ..services.sermon_service import SermonService
from ..services.podcast_service import PodcastService
from ..services.sermon_service import SermonService
from .user_service import UserService


def get_user_service(
    repo: Annotated[UserService, Depends(UserService)],
) -> UserService:
    """
    Returns the Service repo to be used in the api service endpoints.
    """
    return repo


def get_podcast_service(
    repo: Annotated[PodcastService, Depends(PodcastService)],
) -> PodcastService:
    return repo


def get_sermon_service(repo: Annotated[SermonService, Depends(SermonService)]):
    return repo
