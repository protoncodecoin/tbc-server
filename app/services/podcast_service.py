from typing import Annotated, List

from fastapi import Depends, status


from ..repository.podcast_repository import PodcastRepository
from ..schemas.podcast import CreatePodcast, PartialUpdatePodcast, UpdatePodcast
from ..models import Podcast
from ..models.user import User
from ..repository.factory import get_podcast_repo
from ..utils.handler_exceptions import (
    PodcastNotFoundException,
    UnauthoriziedUserException,
)


class PodcastService:
    """Provide business process and algorithms to PodcastRepository."""

    def __init__(self, repo: Annotated[PodcastRepository, Depends(get_podcast_repo)]):
        self.repo = repo

    def insert_podcast(self, podcast: CreatePodcast) -> bool:
        """
        Add new podcast item to the database.
        """
        new_podcast = Podcast(**podcast.model_dump())

        return self.repo.insert_podcast(new_podcast)

    def get_all_podcasts(self, limit: int, offset: int) -> List[Podcast]:
        """
        List all podcast items in the database.
        """
        return self.repo.query_podcast(limit=limit, offset=offset)

    def get_podcast(self, id: int) -> Podcast | None:
        """
        Get a podcast by the given ID.
        """
        return self.repo.query_by_id(id)

    def update_podcast(self, id: int, podcast: UpdatePodcast, user: User) -> bool:
        """
        Update a particular podcast with the given id.
        """
        podcast_obj = Podcast(**podcast.model_dump())
        return self.repo.update_podcast(id, podcast_obj)

    # def partial_update_podcast(
    #     self, id: int, body: PartialUpdatePodcast, user: User
    # ) -> bool:
    #     podcast_obj = self.repo.query_by_id(id)
    #     if podcast_obj is not None:
    #         if podcast_obj.user_id == user.id:

    #             title = getattr(body, "title", None)
    #             running_episodes = getattr(body, "running_episodes", None)

    #             if title is not None:
    #                 podcast_obj.title = title
    #             if running_episodes is not None:
    #                 podcast_obj.running_episodes = running_episodes

    #             return self.repo.update_podcast(podcast_obj)

    #         raise UnauthoriziedUserException(
    #             status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied"
    #         )
    #     raise PodcastNotFoundException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="Podcast Resource not found"
    #     )

    def delete_podcast(self, id: int, user: User) -> bool:
        """
        Delete a podcast by ID
        """

        return self.repo.delete_podcast(id)
