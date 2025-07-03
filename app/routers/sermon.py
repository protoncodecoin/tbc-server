from typing import Annotated, Optional

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Form, File


from ..dependencies import get_current_user
from ..services.factory import get_sermon_service
from ..services.sermon_service import SermonService
from ..schemas.sermon import CreateSermon, ResponseSermon
from ..models.user import User
from ..utils.media_files_handler import save_file
from ..core.constants import SupportedMediaTypePath

router = APIRouter(prefix="/api/v1/sermon", tags=["sermon"])


@router.get("/")
async def get_sermons(
    handler: Annotated[SermonService, Depends(get_sermon_service)],
    limit: Optional[int] = 5,
    offset: Optional[int] = 1,
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

    # updated_sermon.user_id = current_user.id
    cover_path = save_file(file=cover, subdir=SupportedMediaTypePath.IMAGE.name)
    audio_path = save_file(file=audio_file, subdir=SupportedMediaTypePath.AUDIO.name)
    if cover_path is None or audio_path is None:
        raise HTTPException(
            detail="cover or audio can't be empty",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    try:
        new_sermon = CreateSermon(
            theme=theme,
            minister=minister,
            short_note=short_note,
            cover_image=cover_path,
            audio_file=audio_path,
            user_id=current_user.id,
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


@router.get("/{id}/stream")
def stream_sermon(id: int, current_user: Annotated[User, Depends(get_current_user)]):
    """
    Generate audio stream for user.
    """
    return {"message": "done"}


@router.delete("/")
async def delete_sermon(
    id: int, current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Delete a sermon from the database.
    """
    return {"message": "done"}
