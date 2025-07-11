from operator import itemgetter
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
        public_id: str,
    ) -> dict[str, Any]:
        """
        Upload image files to cloudinary
        """

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
        public_id: str,
        folder_name: str,
    ) -> dict[str, Any]:
        """
        Upload large video files to cloudinary
        """

        response: dict[str, Any] = cloudinary.uploader.upload_large(
            file,
            resource_type="auto",
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
        public_id: str,
    ) -> dict[str, Any]:
        """
        Upload audio files to cloudinary
        """

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

    def delete_media_file(
        self,
        public_id: str,
        folder: str,
        resource_type: str | None = None,
    ) -> bool:
        """
        Delete an uploaded media file.
        """
        print(f"{folder}/{public_id}")
        try:
            if resource_type:

                res = cloudinary.uploader.destroy(
                    public_id=f"{folder}/{public_id}",
                    resource_type=resource_type,
                    # folder=folder,
                    # type="authenticated",
                )

            else:
                res = cloudinary.uploader.destroy(
                    public_id=f"{folder}/{public_id}",
                    # folder=folder,
                    # type="authenticated",
                    resource_type=resource_type,
                )

            res_status = itemgetter("result")(res)

            print(res_status, res)

            if res_status == "ok":
                return True
            raise CloudinaryException(
                status_code=400, detail="Failed to delete media file"
            )

        except Exception as e:
            # print(e)
            raise CloudinaryException(
                status_code=400, detail="Failed to delete media file"
            )
        return True

    def create_public_id(self, filename: str) -> str:
        """
        Generate a valid cloudinary public id to be used.
        """
        new_name = filename.strip(" ").replace(" ", "_").split(".")[0]
        return new_name

    def update_media_file(self, public_id: str) -> bool:
        """
        Update a media file.
        """
        pass

    # async def delete_media(self, public_id: str) -> str:
    #     """
    #     Delete media file with given public id.
    #     """
    #     try:
    #         await cloudinary.uploader

    #     except Exception as e:
    #         raise CloudinaryException(
    #             status_code=400, detail="Failed to delete media file."
    #         )


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

# import cloudinary.uploader

# result = cloudinary.uploader.destroy(
#     public_id="audio_folder/song", resource_type="video"
# )

# print(result)
