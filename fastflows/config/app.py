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
    DEFAULT_FLOW_RUNNER_TYPE: str = "subprocess"

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

    # logging
    LOG_LEVEL: str = "DEBUG"
    LOG_PATH: str = "/tmp"
    LOG_FILENAME: str = "fastflows.log"
    LOG_ENQUEUE: bool = True
    LOG_ROTATION: str = "1 days"
    LOG_RETENTION: str = "1 months"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> [id:{extra[request_id]}] - <level>{message}</level>"

    # uvicorn setting
    HOST: str = "0.0.0.0"
    FASTFLOWS_PORT: int = 5010
    RELOAD: bool = True
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
