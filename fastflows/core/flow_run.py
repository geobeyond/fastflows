from fastflows.schemas.prefect.flow_run import (
    StateBase,
    FlowRunResponseGraph,
    FlowRunResponse,
)
from typing import Union
from fastflows.providers import provider


def get_flow_run_details(
    flow_run_id: str, graph: bool = False
) -> Union[FlowRunResponse, FlowRunResponseGraph]:
    """
    :param flow_run_id: Flow Run Id in Prefect to get info about

    """
    if not graph:
        return provider.get_flow_run_details(flow_run_id)
    return provider.get_flow_run_graph(flow_run_id)


def update_flow_run_state(flow_run_id: str, state: StateBase):
    """
    :param flow_run_id: Flow Run Id in Prefect to get info about

    """
    return provider.update_flow_run_state(flow_run_id, state)
