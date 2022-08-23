import datetime
from enum import Enum
from pydantic import BaseModel, Field, Json
from typing import Optional, List, Union
from fastflows.schemas.prefect.misc import Status, Details


class FlowRunStateEnum(str, Enum):

    SCHEDULED = "SCHEDULED"
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class StateDetails(BaseModel):
    flow_run_id: str
    task_run_id: Optional[str]
    child_flow_run_id: Optional[str]
    scheduled_time: Optional[datetime.datetime]
    cache_key: Optional[str]
    cache_expiration: Optional[str]


class StateBase(BaseModel):
    type: FlowRunStateEnum


class FlowRunInput(BaseModel):

    state: Optional[StateBase] = StateBase(type=FlowRunStateEnum.SCHEDULED)
    parameters: Optional[dict] = Field(default_factory=dict)


class FlowRunBlobData(BaseModel):
    data: str
    block_document_id: Optional[str]


class DataObject(BaseModel):
    encoding: str
    blob: Json


class State(StateBase):
    id: str
    name: str
    timestamp: datetime.datetime
    message: Optional[str]
    data: Optional[Union[DataObject, str]]
    state_details: Optional[StateDetails]


class FlowRunState(BaseModel):

    id: str
    state: State


class FlowRunResponse(FlowRunState):
    name: str
    created: datetime.datetime
    updated: datetime.datetime
    name: str
    flow_id: str
    state_id: str
    deployment_id: Optional[str]
    flow_version: Optional[str]
    parameters: dict
    idempotency_key: Optional[str]
    context: dict
    empirical_policy: dict
    empirical_config: dict
    tags: List[str]
    parent_task_run_id: Optional[str]
    state_type: FlowRunStateEnum
    state_name: str
    run_count: int
    expected_start_time: Optional[datetime.datetime]
    next_scheduled_start_time: Optional[datetime.datetime]
    start_time: Optional[datetime.datetime]
    end_time: Optional[datetime.datetime]
    total_run_time: float
    estimated_run_time: float
    estimated_start_time_delta: float
    auto_scheduled: bool


class InitFlowRun(BaseModel):
    name: Optional[str]
    parameters: Optional[dict] = Field(default_factory=dict)
    idempotency_key: Optional[str]
    context: Optional[dict] = Field(default_factory=dict)
    tags: Optional[list] = Field(default_factory=list)
    state: Optional[StateBase]


class UpdateStateResponse(BaseModel):
    # can be null if 'ABORT' status
    state: Optional[State]
    status: Status
    details: Details


class FlowRunResponseGraph(FlowRunState):
    upstream_dependencies: List[Union[str, dict]]
    state_details: Optional[StateDetails]
    expected_start_time: datetime.datetime
    start_time: datetime.datetime
    end_time: datetime.datetime
    total_run_time: int
    estimated_run_time: int
