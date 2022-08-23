import os
from typing import Optional
from pydantic import BaseSettings


class Config(BaseSettings):

    ENV_NAME: Optional[str] = os.environ.get("ENV_NAME")

    # each environment read variables with own prefix
    # to override settings use environment variables
    # with prefix from 'env_prefix' in config
    PREFECT_URI: str = "http://localhost:8080"
    PREFECT_API_TIMEOUT: int = 120
    # must be one of 'local-file-system', 'remote-file-system', 's3', 'gcs', 'azure'"
    PREFECT_STORAGE_BLOCK_TYPE: str = "remote-file-system"
    # it can be main bucket or main path, flows files will be stored in paths like $PREFECT_STORAGE_BASEPATH/flow-name
    PREFECT_STORAGE_BASEPATH: str = "s3://test-bucket"

    # for this name Fastflows will check Block to use to upload flows in Prefect
    PREFECT_STORAGE_NAME: str = "minio6"

    # for remote-file-system
    # should be a json-like string in env variables
    PREFECT_STORAGE_SETTINGS: dict = {
        "key": "0xoznLEXV3JHiOKx",
        "secret": "MmG3vfemCe5mpcxP66a1XvPnsIoXTlWs",
        "client_kwargs": {"endpoint_url": "http://nginx:9000"},
    }

    # must be on of "process"
    PREFECT_INFRASTRUCTURE_BLOCK_TYPE: str = "process"
    # PYGEOAPI URI is used to run flows if provder == Pygeoapi
    PYGEOAPI_URI: str = "http://localhost:8080"
    # config for tags information & parsing flows properties
    VERSION_PREFIX: str = "ver"
    TAG_DELIMITER: str = ":"
    SCHEDULE_PROPERTY: str = "schedule"
    TAGS_PROPERTY: str = "tags"

    # path to search flows
    FLOWS_HOME: str = "flows/"
    # type of flows home directory: local, s3, etc. 'local' only supported from start
    FLOWS_STORAGE_TYPE: str = "local"
    FASTFLOWS_CATALOG_CACHE: str = "./flows/.fastflows"
    FASTFLOWS_AUTO_DEPLOYMENT: int = 1
    FASTFLOW_DEBUG: int = 1
    FASTFLOWS_PROVIDER_PREPARE_AT_THE_START: int = 1

    # logging
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "/tmp"
    LOG_FILENAME: str = "fastflows.log"
    LOG_ENQUEUE: bool = True
    LOG_ROTATION: str = "1 days"
    LOG_RETENTION: str = "1 months"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> [id:{extra[request_id]}] - <level>{message}</level>"

    # uvicorn setting
    FASTFLOWS_HOST: str = "0.0.0.0"
    FASTFLOWS_PORT: int = 5010
    RELOAD: bool = False
    ACCESS_LOG: bool = False
    ROOT_PATH: str = ""

    # auth
    # for test purposes values taken from tests in official repo:
    # https://github.com/busykoala/fastapi-opa/blob/a456f4e6f8f6cb90ca386bbcd5909af3ea44d646/tests/utils.py#L63
    OPA_URL: Optional[str] = ""
    OPA_HOST: Optional[str] = "0.0.0.0"
    OIDC_WELL_KNOWN_ENDPOINT: Optional[str] = "0.0.0.0/.well-known/openid-configuration"
    OIDC_CLIENT_ID: Optional[str] = "example-client"
    OIDC_CLIENT_SECRET: Optional[str] = "secret"

    # env settings
    AWS_LAMBDA_DEPLOY: bool = False

    class Config:
        env_file: str = ".env"
        env_prefix: str = (
            f'{os.environ.get("ENV_NAME")}_' if os.environ.get("ENV_NAME") else ""
        )


configuration = Config()
