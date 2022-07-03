import os


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
    def list(self):
        if not os.path.isdir(self.storage_path):
            raise ValueError(
                f"Flows Home must be a folder. You provided: {self.storage_path}"
            )
        return os.listdir(self.storage_path)

    def read(self):
        pass
