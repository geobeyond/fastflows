import enum
import os
from typing import Optional
from pydantic import BaseModel, BaseSettings
from pathlib import Path


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


class _PrefectRemoteStorageExtraSettings(BaseModel):
    KEY: str = "0xoznLEXV3JHiOKx"
    SECRET: str = "MmG3vfemCe5mpcxP66a1XvPnsIoXTlWs"
    ENDPOINT_URL: str = "http://nginx:9000"


class _PrefectStorage(BaseModel):
    # it can be main bucket or main path, flows files will be stored in paths like $STORAGE_BASEPATH/flow-name
    BASEPATH: str = "s3://test-bucket"
    BLOCK_TYPE: PrefectStorageBlockType = PrefectStorageBlockType.REMOTE_FILE_SYSTEM
    # for this name Fastflows will check Block to use to upload flows in Prefect
    NAME: str = "minio"
    # for remote-file-system
    # should be a json-like string in env variables
    SETTINGS = _PrefectRemoteStorageExtraSettings()


class _PrefectSettings(BaseModel):
    API_TIMEOUT: int = 120
    INFRASTRUCTURE_BLOCK_TYPE: PrefectInfrastructureBlockType = (
        PrefectInfrastructureBlockType.PROCESS
    )
    QUEUE: str = "default"
    URI: str = "http://localhost:8080"
    STORAGE: _PrefectStorage = _PrefectStorage()


class _LoggingSettings(BaseModel):
    ENQUEUE: bool = True
    FILENAME: str = "fastflows.log"
    FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> [id:{extra[request_id]}] - <level>{message}</level>"
    LEVEL: str = "INFO"
    PATH: str = "/tmp"
    RETENTION: str = "1 months"
    ROTATION: str = "1 days"


class _UvicornSettings(BaseModel):
    HOST: str = "0.0.0.0"
    PORT: int = 5010
    RELOAD: bool = False
    ACCESS_LOG: bool = False


class _AuthSettings(BaseModel):
    # auth
    # for test purposes values taken from tests in official repo:
    # https://github.com/busykoala/fastapi-opa/blob/a456f4e6f8f6cb90ca386bbcd5909af3ea44d646/tests/utils.py#L63
    OPA_URL: Optional[str] = ""
    OPA_HOST: Optional[str] = "0.0.0.0"
    OIDC_WELL_KNOWN_ENDPOINT: Optional[str] = "0.0.0.0/.well-known/openid-configuration"
    OIDC_CLIENT_ID: Optional[str] = "example-client"
    OIDC_CLIENT_SECRET: Optional[str] = "secret"


class FastFlowsSettings(BaseSettings):
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
        env_prefix = "FASTFLOWS__"
        env_prefix = (
            f"{env_name}__FASTFLOWS__"
            if (env_name := os.environ.get("ENV_NAME")) is not None
            else "FASTFLOWS__"
        )
        case_sensitive = True
        env_nested_delimiter = "__"


settings = FastFlowsSettings()
