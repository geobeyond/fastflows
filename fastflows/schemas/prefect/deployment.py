# prefect-doc https://orion-docs.prefect.io/concepts/deployments/
import datetime
import uuid
from time import time
from typing import List, Optional, Union

import pydantic

from ...config import settings
from . import misc


class DeploymentInputParams(pydantic.BaseModel):
    """deployment params that can be in input by user"""

    # can be input from rest api
    # properties what can be input by user with cli or REST API
    schedule: Optional[misc.Schedule] = None
    is_schedule_active: bool = True
    parameters: Optional[dict] = {}
    version: Optional[Union[int, str]]
    work_queue_name: Optional[str] = settings.PREFECT.QUEUE
    tags: List[str] = pydantic.Field(default_factory=list)


def generate_deployment_name():
    return datetime.datetime.now().isoformat()


class DeploymentSpec(DeploymentInputParams):

    name: Optional[str] = None
    flow_id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))
    storage_document_id: str
    infra_overrides: dict = {}
    flow_data: Optional[str]
    work_queue_name: Optional[str]
    parameter_openapi_schema: Optional[dict]
    path: Optional[str]
    entrypoint: Optional[str]
    infrastructure_document_id: Optional[str]

    @pydantic.validator("flow_id", "name")
    def not_empty_string(cls, value):  # noqa
        if value.strip() == "":
            raise ValueError("Value cannot be empty string")
        return value

    @pydantic.root_validator(pre=True)
    def generate_tags_and_name(cls, values) -> List[dict]:  # noqa
        if not values.get("version"):
            values["version"] = 1

        if not values.get("tags"):
            values["tags"] = []

        values["tags"].extend(
            [
                f'{settings.VERSION_PREFIX}{settings.TAG_DELIMITER}{values["version"]}',
                f'ts:{str(time()).split(".")[0]}',
            ]
        )
        if not values.get("name"):
            values["name"] = misc.get_hash_from_data(str(values["flow_data"]))

        return values


class DeploymentResponse(DeploymentSpec):

    id: str
    created: datetime.datetime
    updated: datetime.datetime
