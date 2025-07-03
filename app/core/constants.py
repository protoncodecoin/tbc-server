from enum import Enum

SECRET_KEY: str = "faf7037bcfcb9e75c99dd3f421539493d4ca17cb6c4695297182b271295026dc"
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = 90
MEDIA_DIR = "media"


class SupportedMediaTypePath(Enum):
    VIDEO = "videos"
    AUDIO = "audios"
    IMAGE = "images"


AUDIO_FILE_TYPES: list[str] = [
    "aac",
    "he_aac",
    "mp3",
    "ogg",
    "opus",
    "m4a",
    "webm",
]

IMAGE_FILE_TYPES: list[str] = [
    "png",
    "jpeg",
    "jpg",
]


VIDEO_FILE_TYPES: list[str] = [
    "mp4",
    "mov",
    "3gp",  # 3GPP Multimedia File – designed for mobile devices; lower quality
    "mkv",  # Matroska Video – open-source container supporting multiple codecs and subtitles
    "mpeg",  # MPEG-1 or MPEG-2 – used for DVDs and older video formats
    "f4v",
    "m3u8",  # HLS Playlist – used for HTTP Live Streaming
    "ts",  # MPEG Transport Stream – used in broadcasting and streaming
    "dash",  # Dynamic Adaptive Streaming over HTTP – used for adaptive bitrate streaming
    "ismv",
]
