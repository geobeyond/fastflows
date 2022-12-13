from pathlib import Path


class FlowsStorageBase:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

    def list():
        raise NotImplementedError(
            "Flows Storage should implement list method to get all files in flows path directory."
        )

    def read():
        raise NotImplementedError(
            "Flows Storage should implement read method to get flow file content"
        )


class LocalStorage(FlowsStorageBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage_path = Path(self.storage_path)

    def list(self):
        if not self.storage_path.is_dir():
            raise ValueError(
                f"Flows Home must be a folder. You provided: {self.storage_path}"
            )
        return list(self.storage_path.iterdir())

    def read(self):
        pass
