from typing import Any, BinaryIO
import cloudinary.uploader
from typing_extensions import Self
import cloudinary


from app.utils.handler_exceptions import CloudinaryException


class MediaUtils(object):
    def __new__(cls) -> Self:
        if not hasattr(cls, "instance"):
            cls.instance = super(MediaUtils, cls).__new__(cls)
        return cls.instance

    async def upload_image(
        self,
        file: BinaryIO,
        image_name: str,
        folder_name: str,
        public_id: str | None,
    ) -> dict[str, Any]:
        """
        Upload image files to cloudinary
        """
        if public_id is None:
            # generate a public Id from the image name
            public_id = image_name.split(".")[0]

        print("from api: ", public_id)
        response = cloudinary.uploader.upload(
            file,
            public_id=public_id,
            resource_type="image",
            asset_folder=folder_name,
            display_name=image_name,
            # use_filename=True,
            # unique_filename=False,
        )

        return response

    async def upload_video(
        self,
        file: BinaryIO,
        video_name: str,
        public_id: str | None,
        folder_name: str,
    ) -> dict[str, Any]:
        """
        Upload large video files to cloudinary
        """
        if public_id is None:
            public_id = video_name.split(".")[0]

        response: dict[str, Any] = cloudinary.uploader.upload_large(
            file,
            resource_type="video",
            public_id=public_id,
            chunk_size=6_000_000,
            eager_async=True,
            asset_folder=folder_name,
            display_name=video_name,
        )  # type: ignore

        return response

    async def upload_audio(
        self,
        file: BinaryIO,
        audio_name: str,
        folder_name: str,
        public_id: str | None,
    ) -> dict[str, Any]:
        """
        Upload audio files to cloudinary
        """
        if public_id is None:
            public_id = audio_name.split(".")[0]

        print("from api: ", public_id)

        try:
            result: dict[str, Any] = cloudinary.uploader.upload_large(
                file,
                resource_type="auto",
                public_id=public_id,
                chunk_size=6_000_000,
                eager_async=True,
                display_name=audio_name,
                asset_folder=folder_name,
                # user_filename=True,
                # unique_filename=False,
            )  # type: ignore

        except Exception as e:
            raise CloudinaryException(
                status_code=400, detail="Failed to upload media file"
            )

        return result


# singleton to be used across the project
cloudinaryHandler = MediaUtils()


# Upload an image
# upload_result = cloudinary.uploader.upload(
#     "https://res.cloudinary.com/demo/image/upload/getting-started/shoes.jpg",
#     public_id="shoes",
# )
# print(upload_result["secure_url"])

# # Optimize delivery by resizing and applying auto-format and auto-quality
# optimize_url, _ = cloudinary_url("shoes", fetch_format="auto", quality="auto")
# print(optimize_url)

# # Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url(
#     "shoes", width=500, height=500, crop="auto", gravity="auto"
# )
# print(auto_crop_url)
