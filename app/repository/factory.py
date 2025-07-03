"""
Provides a loose coupling design between the repository and service layer.
"""

from typing import Annotated
from fastapi import Depends

from ..repository.sermon_repository import SermonRepository
from .user_repository import UserRepository
from .podcast_repository import PodcastRepository


def get_user_repo(
    repo: Annotated[UserRepository, Depends(UserRepository)],
) -> UserRepository:
    """
    Returns an instance of the user repository.
    """
    return repo


def get_podcast_repo(repo: Annotated[PodcastRepository, Depends(PodcastRepository)]):
    """
    Returns an instance of the podcast repository.
    """
    return repo


def get_sermon_repo(repo: Annotated[SermonRepository, Depends(SermonRepository)]):
    """
    Returns an instance of Sermon Repository."""
    return repo
