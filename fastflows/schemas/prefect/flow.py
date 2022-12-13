import datetime
from pathlib import Path
from typing import List, Optional

import pydantic

from ...config import settings
from .deployment import DeploymentInputParams


# before prefect call
class FlowDeployInput(pydantic.BaseModel):
    """REST Create flow Input model"""

    name: Optional[str]
    flows_home_path: Path = settings.FLOWS_HOME
    flow_data: Optional[str]
    file_path: Optional[Path]
    id: Optional[str]
    flow_base_path: Optional[Path]
    entrypoint: Optional[str]
    deployment_params: Optional[DeploymentInputParams]
    force: bool = pydantic.Field(False, description="Force deploy all flows")
    work_queue_name: Optional[str] = settings.PREFECT.QUEUE


# Flow Data after communication with Prefect
class Flow(pydantic.BaseModel):
    """Created in Prefect Flow with deployment"""

    id: str
    name: str
    file_path: Optional[Path]
    deployment_id: str
    deployment_name: str
    version: int


class PrefectFlowResponse(pydantic.BaseModel):

    name: str
    tags: List[str] = pydantic.Field(default_factory=list)
    id: str
    created: datetime.datetime
    updated: datetime.datetime
