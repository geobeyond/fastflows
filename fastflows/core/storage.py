import fsspec
from fastflows.config.app import configuration as cfg


class S3FileSystem:
    def __init__(self, target_path: str):

        self.fs = fsspec.filesystem(
            "s3",
            key=cfg.PREFECT_STORAGE_SETTINGS["key"],
            secret=cfg.PREFECT_STORAGE_SETTINGS["secret"],
            client_kwargs=cfg.PREFECT_STORAGE_SETTINGS["client_kwargs"],
        )
        self.target_path = target_path

    def upload_files(self, local_path: str):
        self.fs.upload(
            local_path,
            f"{cfg.PREFECT_STORAGE_BASEPATH}/{self.target_path}",
            recursive=True,
        )
