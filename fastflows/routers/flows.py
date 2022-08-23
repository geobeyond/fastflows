from fastapi import APIRouter
from fastflows.schemas.prefect.flow import FlowDeployInput, Flow
from fastflows.schemas.prefect.flow_run import FlowRunInput
from fastflows.core.flow import run_flow, list_flows, get_flow_runs_list, deploy_flows
from fastflows.routers import handle_rest_errors
from typing import List, Optional

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("", response_model=List[Flow])
@handle_rest_errors
async def create_flow_deployment(
    flow_deploy_input: Optional[FlowDeployInput] = FlowDeployInput(),
) -> List[Flow]:
    """if no input - deploy all flows from FLOWS_HOME"""
    # todo: should we separate routes? 1) create flow 2) create deployment
    return deploy_flows(flow_deploy_input)


@router.post("/{flow_id}")
@handle_rest_errors
async def init_flow_run(
    flow_id: str, flow_run_input: Optional[FlowRunInput] = FlowRunInput()
) -> Flow:
    """
    :param flow_id: Flow id in Prefect to run
    """
    return run_flow(flow_id, by_id=True, flow_run_input=flow_run_input)


@router.post("/name/{flow_name}")
@handle_rest_errors
async def init_flow_run_by_name(
    flow_name: str, flow_run_input: Optional[FlowRunInput] = FlowRunInput()
) -> Flow:
    """
    :param flow_name: Flow name in Prefect to run
    """
    return run_flow(flow_name, by_id=False, flow_run_input=flow_run_input)


@router.get("")
@handle_rest_errors
async def list_all_registered_flows_in_fast_flows():
    return list_flows()


@router.get("/{flow_id}/flow_runs")
@handle_rest_errors
async def list_all_flow_runs_by_flow_id(flow_id: str):
    """
    :param flow_id: Flow id in Prefect to run
    """
    return get_flow_runs_list(flow_id, by_id=True)


@router.post("/name/{flow_name}/flow_runs")
@handle_rest_errors
async def list_all_flow_runs_by_flow_name(flow_name: str):
    """
    :param flow_name: Flow id in Prefect to run
    """
    return get_flow_runs_list(flow_name, by_id=False)
