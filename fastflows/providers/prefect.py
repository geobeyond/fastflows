import httpx
from fastflows.config.app import configuration as cfg
from fastflows.providers.base import BaseProvider
from fastflows.schemas.deployment import DeploymentSpec, DeploymentResponse
from fastflows.schemas.flow import PrefectFlowResponse
from fastflows.schemas.flow_data import BaseFlowData
from fastflows.providers.utils import api_response_handler
from fastflows.schemas.flow_run import (
    FlowRunResponse,
    InitFlowRun,
    StateBase,
    UpdateStateResponse,
)
from typing import List, Optional, Dict


class PrefectProvider(BaseProvider):

    uri = f"{cfg.PREFECT_URI}/api"

    def __init__(self) -> None:
        self.client = httpx.Client(timeout=cfg.PREFECT_API_TIMEOUT)

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

    @api_response_handler(...)
    def approve_task(self, flow_run_id: str) -> None:
        """need to implement manual_approve state firstly in Prefect"""
        # response = self.client.post(f"{self.uri}/flow_run_states/{flow_run_id}")
        # return response
        raise NotImplementedError()

    @api_response_handler(
        message="Error while deploying flow. Description:",
    )
    def get_task_run(self, task_run_id: str) -> None:
        """https://orion-docs.prefect.io/api-ref/rest-api/#/Task%20Runs/read_task_run_task_runs__id__get"""

        response = self.client.post(f"{self.uri}/task_runs/{task_run_id}/")
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
            f"{self.uri}/deployments/", json=deployment.dict(exclude={"version"})
        )
        return response

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
        message=f"Prefect does not answer on Healthcheck. Looks like Prefect server is unavailable on address {cfg.PREFECT_URI}",
    )
    def healthcheck(self) -> str:
        response = self.client.get(f"{self.uri}/hello")
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
