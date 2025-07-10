"""
Routers for Podcast.
"""

from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status


from ..dependencies import get_current_user
from ..utils.validators import validate_partial_data
from ..schemas.podcast import (
    CreatePodcast,
    PartialUpdatePodcast,
    UpdatePodcast,
)
from ..models.user import User
from ..services.podcast_service import PodcastService
from ..services.factory import get_podcast_service
from ..utils.handler_exceptions import PodcastNotFoundException

router = APIRouter(tags=["podcast"], prefix="/api/v1/podcasts")


@router.get("/")
async def get_all_podcasts(
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
    limit: Optional[int] = 5,
    offset: Optional[int] = 0,
):
    """Return all podcast.

    Args:
        handler (Annotated[PodcastService, Depends): Provider or dependable for the endpoint

    Returns:
        Podcast: List of podcast objects
    """
    return handler.get_all_podcasts(limit=limit, offset=offset)


@router.get("/{id}")
async def get_podcast(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
):
    query_result = handler.get_podcast(id)
    if query_result is not None:
        return query_result
    raise PodcastNotFoundException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Podcast resource not Found"
    )


@router.post("/", status_code=status.HTTP_200_OK)
async def create_podcast(
    podcast_data: CreatePodcast,
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):

    podcast_data.user_id = current_user.id
    result = handler.insert_podcast(podcast_data)
    if result is False:
        raise HTTPException(
            detail="Failed to create Podcast", status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"status": "successful", "message": "Podcast created successfully"}


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_podcast(
    id: int,
    body: UpdatePodcast,
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    handler.update_podcast(id, body, current_user)
    return {"status": "sucessful", "message": "Podcast updated successfully"}


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def partial_update_podcast(
    id: int,
    body: Annotated[PartialUpdatePodcast, Depends(validate_partial_data)],
    current_user: Annotated[
        User,
        Depends(get_current_user),
    ],
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
):
    """
    Patial Update to Podcast.

    Args:
        id (int): Id of the podcast
    """

    handler.partial_update_podcast(id, body, current_user)
    return {"message": "Updated successfully", "status": "successful"}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_podcast(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
):
    """Delete Podcast.

    Args:
        id (int): Id of the podcast
    """

    handler.delete_podcast(id, current_user)
