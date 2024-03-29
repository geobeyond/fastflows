import typing

from fastapi import APIRouter

from ..schemas.prefect import flow as flow_schemas
from ..schemas.prefect import flow_run as flow_run_schemas
from ..core import flow as flow_ops
from . import handle_rest_errors

router = APIRouter(prefix="/flows", tags=["flows"])


@router.post("", response_model=typing.List[flow_schemas.Flow])
@handle_rest_errors
async def create_flow_deployment(
    flow_deploy_input: flow_schemas.FlowDeployInput,
) -> typing.List[flow_schemas.Flow]:
    """if no input - deploy all flows from FLOWS_HOME"""
    # todo: should we separate routes? 1) create flow 2) create deployment
    return flow_ops.deploy_flows(flow_deploy_input)


@router.post("/{flow_id}")
@handle_rest_errors
async def init_flow_run(
    flow_id: str,
    flow_run_input: typing.Optional[flow_run_schemas.FlowRunInput] = None,
) -> flow_schemas.Flow:
    """:param flow_id: Flow id in Prefect to run"""
    input_ = flow_run_input or flow_run_schemas.FlowRunInput()
    return flow_ops.run_flow(flow_id, by_id=True, flow_run_input=input_)


@router.post("/name/{flow_name}")
@handle_rest_errors
async def init_flow_run_by_name(
    flow_name: str,
    flow_run_input: typing.Optional[flow_run_schemas.FlowRunInput] = None,
) -> flow_schemas.Flow:
    """:param flow_name: Flow name in Prefect to run"""
    input_ = flow_run_input or flow_run_schemas.FlowRunInput()
    return flow_ops.run_flow(flow_name, by_id=False, flow_run_input=input_)


@router.get("")
@handle_rest_errors
async def list_all_registered_flows_in_fast_flows():
    return flow_ops.list_flows()


@router.get("/{flow_id}/flow_runs")
@handle_rest_errors
async def list_all_flow_runs_by_flow_id(flow_id: str):
    """:param flow_id: Flow id in Prefect to run"""
    return flow_ops.get_flow_runs_list(flow_id, by_id=True)


@router.post("/name/{flow_name}/flow_runs")
@handle_rest_errors
async def list_all_flow_runs_by_flow_name(flow_name: str):
    """:param flow_name: Flow id in Prefect to run"""
    return flow_ops.get_flow_runs_list(flow_name, by_id=False)
