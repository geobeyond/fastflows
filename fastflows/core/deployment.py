from typing import Dict

from .blocks import get_or_create_block_document
from ..config import settings
from ..providers import provider
from ..schemas.prefect.deployment import (
    DeploymentSpec,
    DeploymentResponse,
)
from ..schemas.prefect.flow import Flow
from .storage import S3FileSystem


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
    storage.upload_files(flow_input.flow_base_path.as_posix())

    # add deployment to Prefect
    deploy = DeploymentSpec(
        storage_document_id=document_block_id,
        entrypoint=flow_input.entrypoint,
        flow_id=flow_input.id,
        flow_data=flow_input.flow_data,
        work_queue_name=flow_input.work_queue_name or settings.PREFECT.QUEUE,
    )
    return provider.deploy_flow(deploy)
