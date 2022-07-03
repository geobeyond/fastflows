from fastapi import APIRouter
from fastflows.schemas.flow_run import FlowRunState
from fastflows.core.flow_run import (
    update_flow_run_state,
    get_flow_run_details,
)

router = APIRouter(prefix="/flow-runs", tags=["flows"])


@router.get("/{flow_run_id}", response_model=FlowRunState)
async def get_flow_run_details_route(flow_run_id: str):
    """
    :param flow_run_id: Flow Run Id in Prefect to get info about
    """
    return get_flow_run_details(flow_run_id)


@router.patch("/{flow_run_id}", response_model=FlowRunState)
async def update_flow_run_status_route(
    flow_run_id: str,
):
    """
    :param flow_run_id: Flow Run Id in Prefect to update

    """
    return update_flow_run_state(flow_run_id)
