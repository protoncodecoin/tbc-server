import os
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

import cloudinary
from cloudinary.utils import cloudinary_url

from .models.user import Base
from .routers import user, podcast, sermon
from .db.database import engine
from .utils.handler_exceptions import (
    PodcastNotFoundException,
    UnauthoriziedUserException,
    PartialUpdateException,
    CloudinaryException,
    UnknownException,
    DatabaseException,
)
from .core.constants import MEDIA_DIR

from .schemas.config import settings

# Configuration
cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.API_KEY,
    api_secret=settings.API_SECRET,  # Click 'View API Keys' above to copy your API secret
    secure=True,
)


def create_db_tables():
    """
    Create tables if not created
    """
    Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create tables if not created
    """
    # create_db_tables()
    yield


app = FastAPI()


os.makedirs(MEDIA_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router=user.router)
app.include_router(router=podcast.router)
app.include_router(router=sermon.router)


@app.exception_handler(PodcastNotFoundException)
def podcast404_exception_handler(req: Request, ex: PodcastNotFoundException):
    """
    Exception handler for missing podcast resources.
    """
    return JSONResponse(
        status_code=ex.status_code,
        content={
            "message": f"error: {ex.detail}",
        },
    )


@app.exception_handler(UnauthoriziedUserException)
def unauthorizied_exception_handler(req: Request, ex: UnauthoriziedUserException):
    """
    Exception handler for unauthorizied access to podcast resources.
    """
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.exception_handler(PartialUpdateException)
def partial_update_exception_handler(req: Request, ex: PartialUpdateException):
    """
    Exception handler that is raised when no data is included in the patch operation.
    """
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.exception_handler(UnknownException)
def unknown_exception_handler(req: Request, ex: UnknownException):
    """
    Exception handler that is raised when there is an unhandled error.
    """
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.exception_handler(DatabaseException)
def database_exception_handler(req: Request, ex: DatabaseException):
    """
    Exception handler that is raised when there is a database error.
    """
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.exception_handler(CloudinaryException)
def media_upload_exception_handler(req: Request, ex: CloudinaryException):
    """
    Exception handler that is raise when media upload fails.
    """
    return JSONResponse(
        status_code=ex.status_code, content={"message": f"error: {ex.detail}"}
    )


@app.get("/api/v1/")
async def root() -> dict[str, str]:
    return {"message": "Welcome to THE BEAUTIFUL CHURCH API", "version NO.": "1.0"}
