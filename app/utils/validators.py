from fastapi import status

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
