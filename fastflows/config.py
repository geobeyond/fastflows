import enum
import os
from pathlib import Path
from typing import Literal, Optional, Union

import pydantic


class PrefectStorageBlockType(enum.Enum):
    LOCAL_FILE_SYSTEM = "local-file-system"
    REMOTE_FILE_SYSTEM = "remote-file-system"
    S3 = "s3"
    GCS = "gcs"
    AZURE = "azure"


class PrefectInfrastructureBlockType(enum.Enum):
    PROCESS = "process"


class FastFlowsFlowStorageType(enum.Enum):
    LOCAL = "local"


class _PrefectStorage(pydantic.BaseModel):
    BLOCK_NAME: str = "fastflows-storage"


class _PrefectLocalStorage(_PrefectStorage):
    BLOCK_TYPE: Literal["local-file-system"]
    BASE_PATH: Path = Path.home() / "fastflows-prefect-storage"


class _PrefectRemoteStorage(_PrefectStorage):
    BLOCK_TYPE: Literal["remote-file-system"]
    BASE_PATH: pydantic.AnyUrl
    KEY: str
    SECRET: str
    ENDPOINT_URL: str


class _PrefectSettings(pydantic.BaseModel):
    API_TIMEOUT: int = 120
    INFRASTRUCTURE_BLOCK_TYPE: PrefectInfrastructureBlockType = (
        PrefectInfrastructureBlockType.PROCESS
    )
    QUEUE: str = "default"
    URI: str = "http://localhost:4200"
    STORAGE: Union[_PrefectLocalStorage, _PrefectRemoteStorage] = pydantic.Field(
        _PrefectLocalStorage(BLOCK_TYPE="local-file-system"), discriminator="BLOCK_TYPE"
    )

    class Config:
        smart_union = True


class _LoggingSettings(pydantic.BaseModel):
    ENQUEUE: bool = True
    FILENAME: str = "fastflows.log"
    FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> "
        "[id:{extra[request_id]}] - <level>{message}</level>"
    )
    LEVEL: str = "INFO"
    PATH: Path = Path("/tmp")  # noqa
    RETENTION: str = "1 months"
    ROTATION: str = "1 days"


class _UvicornSettings(pydantic.BaseModel):
    HOST: str = "0.0.0.0"  # noqa
    PORT: int = 5010
    RELOAD: bool = False
    ACCESS_LOG: bool = False


class _AuthSettings(pydantic.BaseModel):
    # auth
    # for test purposes values taken from tests in official repo:
    # https://github.com/busykoala/fastapi-opa/blob/a456f4e6f8f6cb90ca386bbcd5909af3ea44d646/tests/utils.py#L63
    OPA_URL: Optional[str] = ""
    OPA_HOST: Optional[str] = "0.0.0.0"  # noqa
    OIDC_WELL_KNOWN_ENDPOINT: Optional[str] = "0.0.0.0/.well-known/openid-configuration"
    OIDC_CLIENT_ID: Optional[str] = "example-client"
    OIDC_CLIENT_SECRET: Optional[str] = "secret"


class FastFlowsSettings(pydantic.BaseSettings):
    AUTH: _AuthSettings = _AuthSettings()
    AUTO_DEPLOYMENT: bool = True
    AWS_LAMBDA_DEPLOY: bool = False
    CATALOG_CACHE: str = "./flows/.fastflows"
    DEBUG: bool = True
    FLOWS_HOME: Path = Path("flows/")
    FLOWS_STORAGE_TYPE: FastFlowsFlowStorageType = FastFlowsFlowStorageType.LOCAL
    PREFECT: _PrefectSettings = _PrefectSettings()
    PROVIDER_PREPARE_AT_THE_START: bool = True
    PYGEOAPI_URI: str = "http://localhost:8080"
    SCHEDULE_PROPERTY: str = "schedule"
    ROOT_PATH: str = ""
    TAG_DELIMITER: str = ":"
    TAGS_PROPERTY: str = "tags"
    VERSION_PREFIX: str = "ver"
    LOGGING: _LoggingSettings = _LoggingSettings()
    UVICORN: _UvicornSettings = _UvicornSettings()

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_nested_delimiter = "__"
        env_prefix = (
            env_name if (env_name := os.environ.get("ENV_NAME", "")) != "" else ""
        )


settings = FastFlowsSettings()
