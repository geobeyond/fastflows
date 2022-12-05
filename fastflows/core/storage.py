import fsspec
from fastflows.config.app import settings


class S3FileSystem:
    def __init__(self, target_path: str):

        self.fs = fsspec.filesystem(
            "s3",
            key=settings.PREFECT.STORAGE.SETTINGS.KEY,
            secret=settings.PREFECT.STORAGE.SETTINGS.SECRET,
            client_kwargs={
                "endpoint_url": settings.PREFECT.STORAGE.SETTINGS.ENDPOINT_URL,
            },
        )
        self.target_path = target_path

    def upload_files(self, local_path: str):
        self.fs.upload(
            local_path,
            f"{settings.PREFECT.STORAGE.BASEPATH}/{self.target_path}",
            recursive=True,
        )
