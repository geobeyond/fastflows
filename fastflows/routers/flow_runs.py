from fastapi import APIRouter
from fastflows.schemas.prefect.flow_run import (
    FlowRunResponse,
    StateBase,
    UpdateStateResponse,
    FlowRunResponseGraph,
)
from fastflows.core.flow_run import (
    update_flow_run_state,
    get_flow_run_details,
)
from typing import List
from fastflows.routers import handle_rest_errors

router = APIRouter(prefix="/flow-runs", tags=["flows"])


@router.get("/{flow_run_id}", response_model=FlowRunResponse)
@handle_rest_errors
async def get_flow_run_details_route(flow_run_id: str):
    """
    :param flow_run_id: Flow Run Id in Prefect to get info about
    """
    return get_flow_run_details(flow_run_id)


@router.get("/{flow_run_id}/graph", response_model=List[FlowRunResponseGraph])
@handle_rest_errors
async def get_flow_run_graph_route(flow_run_id: str):
    """
    :param flow_run_id: Flow Run Id in Prefect to get graph for it
    """
    return get_flow_run_details(flow_run_id, graph=True)


@router.patch("/{flow_run_id}/state", response_model=UpdateStateResponse)
@handle_rest_errors
async def update_flow_run_state_route(
    flow_run_id: str, state: StateBase
) -> UpdateStateResponse:
    """
    :param flow_run_id: Flow Run Id in Prefect to update
    :body state: State to update (example: {'type': 'CANCELLED})
    """
    return update_flow_run_state(flow_run_id, state=state)
