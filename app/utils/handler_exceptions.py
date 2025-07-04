"""
Custom HTTPException for the API Service.
"""

from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException


class PodcastNotFoundException(HTTPException):
    """
    Handle podcast resources that aren't found by api endpoints
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class UnauthoriziedUserException(HTTPException):
    """
    Handle permission errors related to the access of resources
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class PartialUpdateException(HTTPException):
    """
    Thrown when the body contains no data. (Empty Body).
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.headers = headers


class CloudinaryException(HTTPException):
    """
    Thrown when file upload to cloudinary fails.
    """

    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.detail = detail
        self.headers = headers
