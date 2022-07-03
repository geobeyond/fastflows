from fastflows.schemas.flow_run import FlowRunState, FlowRunStateEnum

from fastflows.providers import provider


def get_flow_run_details(flow_run_id: str):
    """
    :param flow_run_id: Flow Run Id in Prefect to get info about

    """
    return provider.get_flow_run_details(flow_run_id)


def update_flow_run_state(flow_run_id: str, state: FlowRunStateEnum):
    """
    :param flow_run_id: Flow Run Id in Prefect to get info about

    """
    # call prefect API

    return FlowRunState(id=flow_run_id, state=FlowRunStateEnum.COMPLETED)
