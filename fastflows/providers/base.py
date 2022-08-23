from fastflows.core.utils.singleton import Singleton


class BaseProvider(metaclass=Singleton):

    type: str = "base"
    uri: str = "provider/api/uri"

    def healthcheck():
        raise NotImplementedError(
            "Healthcheck method should be implemented for each provider"
        )
