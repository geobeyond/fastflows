from typing import List, Optional
from fastflows.schemas.prefect.flow import Flow, FlowDeployInput
from fastflows.schemas.prefect.flow_run import FlowRunResponse, FlowRunInput
from fastflows.errors import FlowNotFound
from fastflows.core.catalog.catalog import catalog, Catalog, catalog_by_id
from fastflows.providers import provider
from fastflows.config.app import configuration as cfg


def get_flow_id(flow_name: str, by_id: bool):
    flow_id = flow_name if by_id else get_flow_by_name(flow_name).id
    return flow_id


def get_flow_by_name(flow_name: str) -> Flow:
    """
        get flow from Catalog, if flow does not exists - try to re-register
    flows & try one more time
    """

    flow = catalog.get(flow_name)

    if not flow:
        flow = register_flow_and_check(flow_name, catalog=catalog)
    return flow


def register_flow_and_check(flow_id: str, catalog: dict) -> Flow:
    # try to register flows, maybe they was updated during runtime
    Catalog().register_and_deploy(FlowDeployInput())
    flow = catalog.get(flow_id)
    if not flow:
        raise FlowNotFound(
            f"Flow was not found in Catalog. Available flows {list(catalog.keys())}"
        )
    return flow


def get_flow_by_id(flow_id: str) -> Flow:
    flow = catalog_by_id.get(flow_id)
    if not flow:
        flow = register_flow_and_check(flow_id, catalog=catalog_by_id)
    return flow


def run_flow(
    flow_name: str, by_id: bool, flow_run_input: FlowRunInput
) -> FlowRunResponse:
    """run flow by name or id"""
    flow_id = get_flow_id(flow_name, by_id)
    flow = get_flow_by_id(flow_id)
    if flow:
        return provider.run_flow(
            deployment_id=flow.deployment_id,
            flow_run_params=flow_run_input,
        )
    else:
        err_message = f"Flow with {'ID' if by_id else 'name'} {flow_name} was not found"
        raise FlowNotFound(err_message)


def get_flow_runs_list(flow_name: str, by_id: bool) -> List[FlowRunResponse]:
    flow_id = get_flow_id(flow_name, by_id)
    return provider.list_flow_runs(flow_id)


def list_flows(flows_home_path: Optional[str] = cfg.FLOWS_HOME) -> List[Flow]:
    # they cannot be registered in Prefect, just list from FLOWS_HOME
    Catalog(flows_home_path=flows_home_path).register_and_deploy()
    return list(catalog.keys())


def deploy_flows(
    flow_input: FlowDeployInput,
) -> List[Flow]:
    return Catalog(flows_home_path=flow_input.flows_home_path).register_and_deploy(
        flow_input
    )
