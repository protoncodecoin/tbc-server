"""
Routers for Podcast.
"""

from datetime import datetime
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File


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
from ..utils.handler_exceptions import (
    PodcastNotFoundException,
    UnauthoriziedUserException,
)
from ..cld_media.media_api import cloudinaryHandler
from ..utils.media_files_handler import validate_file
from ..core.constants import SupportedMediaTypePath


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
    # podcast_data: CreatePodcast,
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    title: str = Form(..., description="Title of the podcast"),
    running_episodes: int = Form(..., description="Episode number"),
    cover_image: UploadFile = File(..., description="Feature Image"),
    video_file: UploadFile = File(..., description="Video file"),
):
    """
    Create podcast file.
    """
    img_public_id = cloudinaryHandler.create_public_id(cover_image.filename)
    video_public_id = cloudinaryHandler.create_public_id(video_file.filename)

    is_valid_image = validate_file(
        file=cover_image, media_type=SupportedMediaTypePath.IMAGE.name
    )
    is_valid_video = validate_file(
        file=video_file, media_type=SupportedMediaTypePath.VIDEO.name
    )

    if not is_valid_image or not is_valid_video:
        raise HTTPException(
            detail="Please provide the valid image or audio file.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    today = datetime.today()

    img_res = await cloudinaryHandler.upload_image(
        file=cover_image.file,
        image_name=cover_image.filename,
        folder_name=f"podcast/images/{today.year}",
        public_id=img_public_id,
    )

    video_res = await cloudinaryHandler.upload_video(
        file=video_file.file,
        video_name=video_file.filename,
        folder_name=f"podcast/videos/{today.year}",
        public_id=video_public_id,
    )

    try:
        new_podcast = CreatePodcast(
            title=title,
            running_episodes=running_episodes,
            user_id=current_user.id,
            cover_image=img_res["url"],
            cld_image_public_id=img_public_id,
            cld_video_public_id=video_public_id,
            video_file=video_res["url"],
        )
    except ValueError as e:
        raise HTTPException(
            detail="Validation error occurred for request. Check if the media type provided matches the approved types.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    result = handler.insert_podcast(new_podcast)
    if result is False:
        raise HTTPException(
            detail="Failed to create Podcast", status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"status": "successful", "message": "Podcast created successfully"}


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_podcast(
    id: int,
    handler: Annotated[PodcastService, Depends(get_podcast_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    title: str = Form(..., description="Title of the podcast"),
    running_episodes: int = Form(..., description="Episode number"),
    cover_image: UploadFile = File(..., description="Feature Image"),
    video_file: UploadFile = File(..., description="Video file"),
    # body: UpdatePodcast,
):
    img_public_id = cloudinaryHandler.create_public_id(cover_image.filename)
    video_public_id = cloudinaryHandler.create_public_id(video_file.filename)

    is_valid_image = validate_file(
        file=cover_image, media_type=SupportedMediaTypePath.IMAGE.name
    )
    is_valid_video = validate_file(
        file=video_file, media_type=SupportedMediaTypePath.VIDEO.name
    )

    if not is_valid_image or not is_valid_video:
        raise HTTPException(
            detail="Please provide the valid image or audio file.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Delete files from cloudinary if the cld_image_public_id and
    # cld_video_public_id aren't the same as the new cld IDs generated

    res_query = handler.get_podcast(id)

    if res_query:
        if res_query.user_id == current_user.id:

            today = datetime.today()
            # if res_query.cld_image_public_id != img_public_id:
            #     # Delete image from cloudinary
            #     cloudinaryHandler.delete_media_file(
            #         public_id=res_query.cld_image_public_id,
            #         resource_type="image",
            #         folder=f"podcast/images/{today.year}",
            #     )

            # if res_query.cld_video_public_id != video_public_id:
            #     # Delete video from cloudinary

            #     cloudinaryHandler.delete_media_file(
            #         public_id=res_query.cld_video_public_id,
            #         resource_type="video",
            #         folder=f"podcast/videos/{today.year}",
            #     )

            img_res = await cloudinaryHandler.upload_image(
                file=cover_image.file,
                image_name=cover_image.filename,
                folder_name=f"podcast/images/{today.year}",
                public_id=img_public_id,
            )

            video_res = await cloudinaryHandler.upload_video(
                file=video_file.file,
                video_name=video_file.filename,
                folder_name=f"podcast/videos/{today.year}",
                public_id=video_public_id,
            )

            try:

                podcast_data = UpdatePodcast(
                    title=title,
                    running_episodes=running_episodes,
                    user_id=current_user.id,
                    cover_image=img_res["url"],
                    cld_image_public_id=img_public_id,
                    cld_video_public_id=video_public_id,
                    video_file=video_res["url"],
                )

            except ValueError as e:
                raise HTTPException(
                    detail="Validation error occurred for request. Check if the media type provided matches the approved types.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            handler.update_podcast(id, podcast_data, current_user)
            return {"status": "sucessful", "message": "Podcast updated successfully"}

        raise UnauthoriziedUserException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied"
        )

    raise PodcastNotFoundException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Podcast resource not Found"
    )


# @router.patch("/{id}", status_code=status.HTTP_200_OK)
# async def partial_update_podcast(
#     id: int,
#     body: Annotated[PartialUpdatePodcast, Depends(validate_partial_data)],
#     current_user: Annotated[
#         User,
#         Depends(get_current_user),
#     ],
#     handler: Annotated[PodcastService, Depends(get_podcast_service)],
# ):
#     """
#     Patial Update to Podcast.

#     Args:
#         id (int): Id of the podcast
#     """

#     handler.partial_update_podcast(id, body, current_user)
#     return {"message": "Updated successfully", "status": "successful"}


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

    res_query = handler.get_podcast(id)
    if res_query:
        if res_query.user_id == current_user.id:
            return handler.delete_podcast(id, current_user)

        raise UnauthoriziedUserException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission denied"
        )
    raise PodcastNotFoundException(
        detail="Podcast Resource not Found", status_code=status.HTTP_404_NOT_FOUND
    )
