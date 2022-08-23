from fastflows.providers import provider
from typing import Dict
from fastflows.schemas.prefect.deployment import DeploymentResponse

from fastflows.core.blocks import get_or_create_block_document
from fastflows.core.storage import S3FileSystem
from fastflows.schemas.prefect.flow import Flow
from fastflows.schemas.prefect.deployment import DeploymentSpec


def get_last_deployments_per_flow() -> Dict[str, DeploymentResponse]:
    deployments_from_prefect = provider.get_deployments()

    deployments_by_flow_id = {}

    for deployment in deployments_from_prefect:
        deployments_by_flow_id[deployment.flow_id] = deployment
    return deployments_by_flow_id


def create_flow_deployment(flow_input: Flow) -> DeploymentResponse:
    """deploy flow (per flow)"""
    # create block document
    document_block_id = get_or_create_block_document(flow_input.name)

    # upload flow documents to s3
    storage = S3FileSystem(flow_input.name)
    storage.upload_files(flow_input.flow_base_path)

    # add deployment to Prefect
    deploy = DeploymentSpec(
        storage_document_id=document_block_id,
        entrypoint=flow_input.entrypoint,
        flow_id=flow_input.id,
        flow_data=flow_input.flow_data,
    )
    return provider.deploy_flow(deploy)
