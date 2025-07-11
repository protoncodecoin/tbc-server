from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Form, File

from datetime import datetime

from ..dependencies import get_current_user
from ..services.factory import get_sermon_service
from ..services.sermon_service import SermonService
from ..schemas.sermon import CreateSermon, UpdateSermon
from ..models.user import User
from ..utils.media_files_handler import validate_file
from ..core.constants import SupportedMediaTypePath
from ..cld_media.media_api import cloudinaryHandler
from ..utils.handler_exceptions import (
    DatabaseException,
    UnauthoriziedUserException,
)
from ..utils.validators import validate_sermon_partial_data

router = APIRouter(prefix="/api/v1/sermon", tags=["sermon"])


@router.get("/")
async def get_sermons(
    current_user: Annotated[User, Depends(get_current_user)],
    handler: Annotated[SermonService, Depends(get_sermon_service)],
    limit: Optional[int] = 5,
    offset: Optional[int] = 0,
):
    """
    Get all sermons.
    """
    return handler.get_sermons(limit=limit, offset=offset)


@router.post("/")
async def create_sermon(
    handler: Annotated[SermonService, Depends(get_sermon_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    theme: str = Form(..., description="Theme for the service", max_length=250),
    minister: str = Form(..., description="The preacher", max_length=70),
    short_note: str = Form(
        ...,
        description="A brief description or information about the service",
        max_length=200,
    ),
    cover: UploadFile = File(..., description="Cover image"),
    audio_file: UploadFile = File(..., description="Audio file"),
):
    """
    Create new sermon.
    """

    audio_public_id = cloudinaryHandler.create_public_id(audio_file.filename)  # type: ignore
    img_public_id = cloudinaryHandler.create_public_id(cover.filename)  # type: ignore

    # # updated_sermon.user_id = current_user.id
    is_valid_image = validate_file(
        file=cover, media_type=SupportedMediaTypePath.IMAGE.name
    )
    is_valid_audio = validate_file(
        file=audio_file, media_type=SupportedMediaTypePath.AUDIO.name
    )

    if not is_valid_image or not is_valid_audio:
        raise HTTPException(
            detail="Please provide the valid image or audio file.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    today = datetime.today()
    # upload image and audio to cloudinary
    img_res = await cloudinaryHandler.upload_image(
        file=cover.file,
        image_name=cover.filename,  # type: ignore
        folder_name=f"sermon/images/{today.year}",
        public_id=img_public_id,
    )

    audio_res = await cloudinaryHandler.upload_audio(
        file=audio_file.file,
        audio_name=audio_file.filename,  # type: ignore
        folder_name=f"sermon/audios/{today.year}",
        public_id=audio_public_id,
    )

    try:
        new_sermon = CreateSermon(
            theme=theme,
            minister=minister,
            short_note=short_note,
            cover_image=img_res["url"],
            audio_file=audio_res["url"],
            user_id=current_user.id,
            cld_image_public_id=img_public_id,
            cld_audio_public_id=audio_public_id,
        )
    except ValueError as e:

        raise HTTPException(
            detail="Validation error occurred for request. Check if the media type provided matches the approved types.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    result = handler.insert_sermon(new_sermon)
    if not result:
        raise HTTPException(
            detail="Failed to create sermon", status_code=status.HTTP_400_BAD_REQUEST
        )
    return {"status": "successful", "message": "Sermon created successfully"}


@router.get("/{id}/")
def get_sermon(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    handler: Annotated[SermonService, Depends(get_sermon_service)],
):
    """
    Generate audio stream for user.
    """
    res = handler.get_single_sermon(id)
    if res is None:
        raise HTTPException(
            detail="Resource not found", status_code=status.HTTP_404_NOT_FOUND
        )
    if res:
        return res

    raise DatabaseException(
        detail="An error occurred", status_code=status.HTTP_404_NOT_FOUND
    )


@router.delete("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_sermon(
    id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    handler: Annotated[SermonService, Depends(get_sermon_service)],
):
    """
    Delete a sermon from the database.
    """
    # res = handler.delete_sermon(id)
    res = handler.get_single_sermon(id)
    if res:
        print(res.cld_image_public_id, res.cld_audio_public_id)
        # Delete media files from cloudinary
        img_res = cloudinaryHandler.delete_media_file(res.cld_image_public_id)
        audio_res = cloudinaryHandler.delete_media_file(
            res.cld_audio_public_id, resource_type="video"
        )

        if img_res and audio_res:
            # if img_res and audio_res:
            return handler.delete_sermon(id)

    if res is None:
        raise HTTPException(
            detail="Resource not found", status_code=status.HTTP_404_NOT_FOUND
        )

    # handler returns false if there is a database errror
    if not res:

        raise DatabaseException(
            detail="An error occurred", status_code=status.HTTP_404_NOT_FOUND
        )


@router.put("/{id}/", status_code=status.HTTP_200_OK)
async def update(
    id: int,
    handler: Annotated[SermonService, Depends(get_sermon_service)],
    current_user: Annotated[User, Depends(get_current_user)],
    theme: str = Form(..., description="Theme for the service", max_length=250),
    minister: str = Form(..., description="The preacher", max_length=70),
    short_note: str = Form(
        ...,
        description="A brief description or information about the service",
        max_length=200,
    ),
    cover: UploadFile = File(..., description="Cover image"),
    audio_file: UploadFile = File(..., description="Audio file"),
) -> dict[str, str]:
    """
    Perform a full update to resource.
    """

    res = handler.get_single_sermon(id)

    if res:

        if res.user_id == current_user.id:

            audio_public_id = cloudinaryHandler.create_public_id(audio_file.filename)
            img_public_id = cloudinaryHandler.create_public_id(cover.filename)

            # # updated_sermon.user_id = current_user.id
            today = datetime.today()
            is_valid_image = validate_file(
                file=cover, media_type=SupportedMediaTypePath.IMAGE.name
            )
            is_valid_audio = validate_file(
                file=audio_file, media_type=SupportedMediaTypePath.AUDIO.name
            )

            if not is_valid_image or not is_valid_audio:
                raise HTTPException(
                    detail="Please provide the valid image or audio file.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            if res.cld_image_public_id != img_public_id:
                cloudinaryHandler.delete_media_file(
                    public_id=res.cld_image_public_id, resource_type="image"
                )

            if res.cld_audio_public_id != audio_public_id:
                cloudinaryHandler.delete_media_file(
                    public_id=res.cld_audio_public_id,
                    resource_type="video",
                )

            # upload image and audio to cloudinary
            img_res = await cloudinaryHandler.upload_image(
                file=cover.file,
                image_name=cover.filename,  # type: ignore
                folder_name=f"sermon/images/{today.year}",
                public_id=img_public_id,
            )

            audio_res = await cloudinaryHandler.upload_audio(
                file=audio_file.file,
                audio_name=audio_file.filename,  # type: ignore
                folder_name=f"sermon/audios/{today.year}",
                public_id=audio_public_id,
            )

            try:
                sermon_data = UpdateSermon(
                    theme=theme,
                    minister=minister,
                    short_note=short_note,
                    cover_image=img_res["url"],
                    audio_file=audio_res["url"],
                    user_id=current_user.id,
                    cld_image_public_id=img_public_id,
                    cld_audio_public_id=audio_public_id,
                )
            except ValueError as e:

                raise HTTPException(
                    detail="Validation error occurred for request. Check if the media type provided matches the approved types.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                )

            res = handler.update_sermon(id, sermon_data)
            return {"message": "ok"}

        raise UnauthoriziedUserException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied"
        )

    raise HTTPException(
        detail="Resource not found",
        status_code=status.HTTP_400_BAD_REQUEST,
    )


# @router.patch("/{id}/")
# async def partial_update(
#     id: int,
#     handler: Annotated[
#         SermonService,
#         Depends(get_sermon_service),
#     ],
#     cover: UploadFile = File(description="Cover image", default=None),
#     # validate_data=Depends(validate_sermon_partial_data),
# ):
#     """
#     Partial update to sermon.
#     """
#     print(cover)
#     res = handler.get_sermons(id)

#     if res:

#         return {"msg": "ok"}

#     raise HTTPException(
#         detail="Resource not found",
#         status_code=status.HTTP_400_BAD_REQUEST,
#     )
