from fastapi import status
from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    UploadFile,
    Form,
    File,
    Request,
)


from ..utils.handler_exceptions import PartialUpdateException
from ..schemas.podcast import PartialUpdatePodcast


def validate_partial_data(body: PartialUpdatePodcast) -> PartialUpdatePodcast:
    """
    Validate body data for patch method.
    """
    title = getattr(body, "title", None)
    running_episodes = getattr(body, "running_episodes", None)

    if title is None and running_episodes is None:
        raise PartialUpdateException(
            detail="At least one data attribute should be provided",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    podcast_data = PartialUpdatePodcast()
    if title:
        podcast_data.title = title
    if running_episodes:
        podcast_data.running_episodes = running_episodes
    return podcast_data


def validate_sermon_partial_data(
    # id: int,
    request: Request,
    theme: str = Form(
        description="Theme for the service", max_length=250, default=None
    ),
    minister: str = Form(
        description="The preacher's name", max_length=70, default=None
    ),
    short_note: str = Form(
        description="A brief description or information about the service",
        max_length=200,
        default=None,
    ),
    # cover: UploadFile = File(description="Cover image", default=None),
    # audio_file: UploadFile = File(description="Audio file", default=None),
):
    """
    Validate partial data for sermon endpoint.
    """

    id = request.path_params["id"]
    if id is None:
        raise HTTPException(
            detail="Resource not found",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if (
        theme == ""
        and minister == ""
        and short_note == ""
        # and cover == ""
        # and audio_file == ""
    ):
        raise HTTPException(
            detail="At least one data has to be present in request body.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    return {"ok": "msg"}
