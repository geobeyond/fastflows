import typing
from pathlib import Path

from ..config import settings
from .. import (
    errors,
    providers,
)
from ..schemas.prefect import (
    flow as flow_schemas,
    flow_run as flow_run_schemas,
)
from .catalog import catalog as catalog_module


def get_flow_id(flow_name: str, by_id: bool):
    flow_id = flow_name if by_id else get_flow_by_name(flow_name).id
    return flow_id


def get_flow_by_name(flow_name: str) -> flow_schemas.Flow:
    """Retrieve flow by name.

    get flow from Catalog, if flow does not exist - try to re-register flows & try one
    more time
    """
    flow = catalog_module.catalog.get(flow_name)

    if not flow:
        flow = register_flow_and_check(flow_name, catalog_=catalog_module.catalog)
    return flow


def register_flow_and_check(flow_id: str, catalog_: dict) -> flow_schemas.Flow:
    # try to register flows, maybe they were updated during runtime
    catalog_module.Catalog().register_and_deploy()
    flow = catalog_.get(flow_id)
    if not flow:
        raise errors.FlowNotFoundError(
            f"Flow was not found in Catalog. Available flows {list(catalog_.keys())}"
        )
    return flow


def get_flow_by_id(flow_id: str) -> flow_schemas.Flow:
    flow = catalog_module.catalog_by_id.get(flow_id)
    if not flow:
        flow = register_flow_and_check(flow_id, catalog_=catalog_module.catalog_by_id)
    return flow


def run_flow(
    flow_name: str, by_id: bool, flow_run_input: flow_run_schemas.FlowRunInput
) -> flow_run_schemas.FlowRunResponse:
    """run flow by name or id"""
    flow_id = get_flow_id(flow_name, by_id)
    flow = get_flow_by_id(flow_id)
    if flow:
        return providers.provider.run_flow(
            deployment_id=flow.deployment_id,
            flow_run_params=flow_run_input,
        )
    else:
        err_message = f"Flow with {'ID' if by_id else 'name'} {flow_name} was not found"
        raise errors.FlowNotFoundError(err_message)


def get_flow_runs_list(
    flow_name: str, by_id: bool
) -> typing.List[flow_run_schemas.FlowRunResponse]:
    flow_id = get_flow_id(flow_name, by_id)
    return providers.provider.list_flow_runs(flow_id)


def list_flows(
    flows_home_path: typing.Optional[Path] = settings.FLOWS_HOME,
) -> typing.List[str]:
    # they cannot be registered in Prefect, just list from FLOWS_HOME
    catalog_module.Catalog(flows_home_path=flows_home_path).register_and_deploy()
    return list(catalog_module.catalog.keys())


def deploy_flows(
    flow_input: flow_schemas.FlowDeployInput,
) -> typing.List[flow_schemas.Flow]:
    return catalog_module.Catalog(
        flows_home_path=flow_input.flows_home_path
    ).register_and_deploy(flow_input)
