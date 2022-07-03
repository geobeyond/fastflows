from enum import Enum
from pydantic import BaseModel


class TaskState(Enum):

    # possible list of task states from Prefect
    PENDING = "pending"
    QUEUED = "queued"
    RETRYING = "retrying"
    RUNNING = "running"
    CACHED = "cached"
    FINISHED = "finished"
    LOOPED = "looped"
    SCHEDULED = "scheduled"
    SUBMITTED = "submitted"
    SKIPPED = "skipped"
    SUCCESS = "success"
    FAILED = "failed"
    MAPPED = "mapped"


class TaskRunState(BaseModel):
    id: str
    state: TaskState
