from pydantic import BaseModel, Field, root_validator
from enum import Enum
from fastflows.schemas.misc import get_hash_from_data, Schedule
from typing import Optional, List


# Flow Data from file or input
class Encodings(str, Enum):

    TEXT = "text"
    JSON = "json"
    CLOUDPICKLE = "cloudpickle"
    BLOCKSTORAGE = "blockstorage"


class ScheduleFromFile(Schedule):
    lineno: int


class FlowData(BaseModel):

    encoding: Encodings = Encodings.TEXT.value
    blob: str


class BaseFlowData(BaseModel):
    """Base class for flow data"""

    name: str
    tags: List[str] = Field(default_factory=list)


class FlowDataFromFile(BaseFlowData):
    """model to store information from Flow File"""

    file_path: Optional[str]
    flow_data: Optional[FlowData]
    # file_modified can be None if flow data from user input
    file_modified: Optional[int]
    schedule: Optional[Schedule]
    # hash from file/flow code (md5)
    deployment_name: Optional[str]

    @root_validator(pre=True)
    def generate_deployment_name(cls, values: dict) -> dict:
        values["deployment_name"] = get_hash_from_data(values["flow_data"].blob)
        return values


class TagsFromFile(BaseModel):
    tags: List[str]
    lineno: int
