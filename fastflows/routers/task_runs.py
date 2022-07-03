from fastapi import APIRouter
from fastflows.schemas.task_run import TaskRunState
from fastflows.core.task_run import update_task_run_state

router = APIRouter(prefix="/task-runs", tags=["task-runs"])


@router.patch("/{task_id}", response_model=TaskRunState)
async def update_task_run_state_route(task_run_id: str):
    """
    :param flow_run_id: Flow Run Id in Prefect
    :param task_id: Task Id to update

    """
    return update_task_run_state(task_run_id)
