from typing import Annotated, List

from fastapi import Depends


from ..repository.sermon_repository import SermonRepository
from ..repository.factory import get_sermon_repo
from ..models.user import User
from ..schemas.sermon import CreateSermon
from ..models.sermon import Sermon


class SermonService:
    """
    Business logic for Sermon repository.
    """

    def __init__(
        self, repo: Annotated[SermonRepository, Depends(get_sermon_repo)]
    ) -> None:
        self.repo = repo

    def insert_sermon(self, sermon: CreateSermon):
        """
        Inset sermon object to db.
        """
        new_sermon = Sermon(**sermon.model_dump())

        return self.repo.insert_sermon(new_sermon)

    def get_sermons(self, limit=None, offset=None) -> List[Sermon]:
        """
        Returns a list of sermon objects.
        """
        return self.repo.query_sermons(limit=limit, offset=offset)

    def delete_sermon(self, id: int) -> bool:
        """
        Delete sermon with the given Id
        """
        return self.repo.delete_sermon(id)
