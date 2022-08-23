import httpx
from fastflows.config.app import configuration as cfg
from fastflows.providers.base import BaseProvider
from fastflows.schemas.prefect.deployment import DeploymentSpec, DeploymentResponse
from fastflows.schemas.prefect.block import (
    BlockDocumentInput,
    BlockDocumentResponse,
    BlockTypeResponse,
    BlockSchemaResponse,
)
from fastflows.schemas.prefect.flow import PrefectFlowResponse
from fastflows.schemas.prefect.flow_data import BaseFlowData
from fastflows.providers.utils import api_response_handler
from fastflows.schemas.prefect.flow_run import (
    FlowRunResponse,
    InitFlowRun,
    StateBase,
    UpdateStateResponse,
    FlowRunResponseGraph,
)
from typing import List, Optional, Dict


class Flows:
    @api_response_handler(
        message="Cannot run the flow with flow_id {}",
    )
    def run_flow(
        self, deployment_id: str, flow_run_params: InitFlowRun
    ) -> FlowRunResponse:

        return self.client.post(
            f"{self.uri}/deployments/{deployment_id}/create_flow_run",
            json=flow_run_params.dict(),
        )

    @api_response_handler(
        message="Error while creating new Flow.",
    )
    def create_flow(self, flow_request: BaseFlowData) -> PrefectFlowResponse:
        response = self.client.post(f"{self.uri}/flows/", json=flow_request.dict())
        return response

    @api_response_handler(
        message="Error during getting all flows from Prefect",
        response_model=List[PrefectFlowResponse],
    )
    def get_flows(self, filters: Optional[Dict] = None) -> List[PrefectFlowResponse]:
        response = self.client.post(f"{self.uri}/flows/filter", json=filters or {})
        return response


class Deployments:
    @api_response_handler(
        message="Error during getting all deployments from Prefect",
        response_model=List[DeploymentResponse],
    )
    def get_deployments(
        self, filters: Optional[Dict] = None
    ) -> List[DeploymentResponse]:
        response = self.client.post(
            f"{self.uri}/deployments/filter", json=filters or {}
        )
        return response

    @api_response_handler(
        message="Error while deleting deployment by_id",
    )
    def deploy_flow(self, deployment: DeploymentSpec) -> DeploymentResponse:
        """
        call deployment API:
            https://orion-docs.prefect.io/api-ref/rest-api/#/Deployments/create_deployment_deployments__post

            :param deployment: Deployment configuration

        """

        response = self.client.post(
            f"{self.uri}/deployments/", json=deployment.dict(exclude={"flow_data"})
        )
        return response


class FlowRuns:
    @api_response_handler(
        message="Error while getting Flow Runs by flow_id.",
        response_model=List[FlowRunResponse],
    )
    def list_flow_runs(self, flow_id: str) -> List[FlowRunResponse]:
        payload = {"flows": {"id": {"any_": [flow_id]}}}
        response = self.client.post(
            f"{self.uri}/flow_runs/filter",
            json=payload,
        )
        return response

    @api_response_handler(
        message="Error while getting FlowRun details.",
        append_api_error=True,
        response_model=List[FlowRunResponse],
    )
    def get_flow_run_details(self, flow_run_id: str) -> List[FlowRunResponse]:
        response = self.client.get(f"{self.uri}/flow_runs/{flow_run_id}")
        return response

    @api_response_handler(
        message="Error while getting FlowRun graph.",
        append_api_error=True,
        response_model=List[FlowRunResponseGraph],
    )
    def get_flow_run_graph(self, flow_run_id: str) -> List[FlowRunResponseGraph]:
        response = self.client.get(f"{self.uri}/flow_runs/{flow_run_id}/graph")
        return response

    @api_response_handler(
        message="Error while updating FlowRun state.",
    )
    def update_flow_run_state(
        self, flow_run_id: str, state: StateBase
    ) -> UpdateStateResponse:
        response = self.client.post(
            f"{self.uri}/flow_runs/{flow_run_id}/set_state",
            json={"state": state.dict()},
        )
        return response


class Tasks:
    @api_response_handler(...)
    def approve_task(self, flow_run_id: str) -> None:
        """need to implement manual_approve state firstly in Prefect"""
        raise NotImplementedError()

    @api_response_handler(
        message="Error while deploying flow. Description:",
    )
    def get_task_run(self, task_run_id: str) -> None:
        """https://orion-docs.prefect.io/api-ref/rest-api/#/Task%20Runs/read_task_run_task_runs__id__get"""

        response = self.client.post(f"{self.uri}/task_runs/{task_run_id}/")
        return response


class Blocks:
    @api_response_handler(
        message="Problem with reading Block Document by name",
    )
    def read_block_document_by_name(
        self, document_name: str, slug: str = cfg.PREFECT_STORAGE_BLOCK_TYPE
    ) -> BlockDocumentResponse:
        return self.client.get(
            f"{self.uri}/block_types/slug/{slug}/block_documents/name/{document_name}"
        )

    @api_response_handler(
        message="Problem with creating Block Document",
    )
    def create_block_document(
        self, block_data: BlockDocumentInput
    ) -> BlockDocumentResponse:

        response = self.client.post(
            f"{self.uri}/block_documents/", json=block_data.dict()
        )

        return response

    @api_response_handler(
        message="Problem with getting Block Type",
    )
    def get_block_by_slug(self, slug: str) -> BlockTypeResponse:

        response = self.client.get(f"{self.uri}/block_types/slug/{slug}")
        return response

    @api_response_handler(
        message="Problem with getting Block Schema by Block Type ID",
        response_model=BlockSchemaResponse,
    )
    def get_block_schema_by_type_id(
        self, block_type_id: str
    ) -> List[BlockSchemaResponse]:

        response = self.client.post(
            f"{self.uri}/block_schemas/filter",
            json={
                "block_schemas": {
                    "operator": "and_",
                    "block_type_id": {"any_": [block_type_id]},
                }
            },
        )
        return response


class PrefectProvider(BaseProvider, Blocks, Flows, Deployments, FlowRuns, Tasks):

    type: str = "prefect"

    uri: str = f"{cfg.PREFECT_URI}/api"

    def __init__(self) -> None:
        self.client = httpx.Client(timeout=cfg.PREFECT_API_TIMEOUT)

    @api_response_handler(
        message=f"Prefect does not answer on Healthcheck. Looks like Prefect server is unavailable on address {cfg.PREFECT_URI}",
    )
    def healthcheck(self) -> str:
        response = self.client.get(f"{self.uri}/hello")
        return response
