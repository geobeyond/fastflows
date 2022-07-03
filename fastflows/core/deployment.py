from fastflows.providers import provider
from typing import Dict
from fastflows.schemas.deployment import DeploymentResponse


def get_last_deployments_per_flow() -> Dict[str, DeploymentResponse]:
    deployments_from_prefect = provider.get_deployments()

    deployments_by_flow_id = {}

    for deployment in deployments_from_prefect:
        deployments_by_flow_id[deployment.flow_id] = deployment
    return deployments_by_flow_id
