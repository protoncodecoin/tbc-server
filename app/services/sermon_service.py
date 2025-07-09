from typing import Annotated, List

from fastapi import Depends


from ..repository.sermon_repository import SermonRepository
from ..repository.factory import get_sermon_repo
from ..schemas.sermon import CreateSermon, UpdateSermon
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

    def get_single_sermon(self, id: int) -> Sermon | None:
        """
        Return a single sermon.
        """
        return self.repo.query_sermon(id)

    def delete_sermon(self, id: int) -> bool | None:
        """
        Delete sermon with the given Id
        """
        return self.repo.delete_sermon(id)

    def update_sermon(self, id: int, sermon: UpdateSermon) -> bool:
        """
        Update a sermon with the given id.
        """
        updated_data = Sermon(**sermon.model_dump())

        return self.repo.update_sermon(id, updated_data)
