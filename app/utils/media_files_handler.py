import os
import shutil
from uuid import uuid4

from fastapi import UploadFile

from ..core.constants import (
    MEDIA_DIR,
    IMAGE_FILE_TYPES,
    AUDIO_FILE_TYPES,
    VIDEO_FILE_TYPES,
    SupportedMediaTypePath,
)


def save_file(file: UploadFile, subdir: str) -> str | None:
    """
    Return file path to be saved in DB.
    """
    if file:
        ran_num = uuid4()
        file_ext = file.filename.split(".")[-1]  # type: ignore

        if subdir == SupportedMediaTypePath.AUDIO.name:
            if file_ext not in AUDIO_FILE_TYPES:
                raise ValueError("File extension not supported")
        if subdir == SupportedMediaTypePath.IMAGE.name:
            if file_ext not in IMAGE_FILE_TYPES:
                raise ValueError("File extension not supported")
        if subdir == SupportedMediaTypePath.VIDEO.name:
            if file_ext not in VIDEO_FILE_TYPES:
                raise ValueError("File extension not supported")

        file.filename = (
            file.filename.split(".")[0] + "-" + str(ran_num) + "." + file_ext  # type: ignore
        )
        folder = os.path.join(MEDIA_DIR, subdir)
        os.makedirs(folder, exist_ok=True)
        file_path = os.path.join(folder, file.filename)  # type: ignore
        print("file_path is: ", file_path)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_path
    return None


def validate_file(file: UploadFile, media_type: str) -> bool:
    """
    Return file path to be saved in DB.
    """
    if file:
        file_ext = file.filename.split(".")[-1]  # type: ignore

        if media_type == SupportedMediaTypePath.AUDIO.name:
            if file_ext in AUDIO_FILE_TYPES:
                return True
        if media_type == SupportedMediaTypePath.IMAGE.name:
            if file_ext in IMAGE_FILE_TYPES:
                return True
        if media_type == SupportedMediaTypePath.VIDEO.name:
            if file_ext in VIDEO_FILE_TYPES:
                return True
        return False

    return False
