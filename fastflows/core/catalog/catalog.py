import os
import logging
from fastflows.errors import FlowNotFound
from fastflows.config.app import configuration as cfg
from fastflows.core.deployment import (
    get_last_deployments_per_flow,
    create_flow_deployment,
)
from fastflows.core.catalog.storage import LocalStorage
from fastflows.core.catalog.reader import FlowFileReader
from fastflows.schemas.prefect.flow import Flow, PrefectFlowResponse, FlowDeployInput
from fastflows.schemas.prefect.flow_data import FlowDataFromFile, BaseFlowData
from fastflows.providers import provider
from fastflows.core.catalog.cache import CatalogCache
from fastflows.core.utils.singleton import Singleton
from fastflows.schemas.prefect.deployment import (
    DeploymentResponse,
)
from typing import List, Optional, Dict, Union


class Catalog(metaclass=Singleton):
    """main class to register all flows"""

    # because class is singleton - always will be one instance
    catalog: Dict[str, Flow] = {}
    catalog_by_id: Dict[str, Flow] = {}

    storages = {
        # add here API to work with flows on S3, or any other store
        "local": LocalStorage
    }

    def __init__(
        self,
        flows_home_path: str = cfg.FLOWS_HOME,
        storage_type: str = cfg.FLOWS_STORAGE_TYPE,
    ) -> None:

        self.flows_home_path = flows_home_path
        self.storage_type = storage_type
        self.cache = CatalogCache()
        self.get_catalog_from_cache()

    def _get_storage(self):
        storage = self.storages.get(self.storage_type)
        if storage is None:
            raise Exception(
                f"Flows storage type is not supported. Must be one of: {self.storages}"
            )
        return storage(self.flows_home_path)

    def get_flow_data(self, flow_file_path: str) -> str:
        with open(flow_file_path) as f:
            return f.read()

    def get_catalog_from_cache(self):
        cached_data = self.cache.read()
        for flow_name, flow_data in cached_data.items():
            flow = Flow(**flow_data)
            self.catalog[flow_name] = flow
            self.catalog_by_id[flow_data["id"]] = flow

    def set_flows_path(self, new_path: str) -> None:
        # method to use in test
        self.flows_home_path = new_path

    def _blob_data_processing(self, flow_data: str) -> str:

        flow_file = FlowFileReader(flow_data=flow_data)

        if not flow_file.is_flows:
            # file exists, but there is no flow inside
            raise FlowNotFound("Flow was not found in provided data")

        return flow_file.flows

    def _flow_path_processing(self, flow_path: str) -> str:

        # to have absolute path
        if self.flows_home_path not in flow_path:
            flow_path = os.path.join(self.flows_home_path, flow_path)

        if not os.path.exists(flow_path):
            # file does not exist
            raise FlowNotFound(f"Flow path '{flow_path}' does not exist'")

        flow_file = FlowFileReader(file_path=flow_path)

        if not flow_file.is_flows:
            # file exists, but there is no flow inside
            raise FlowNotFound(f"Flow was not found in file with path '{flow_path}''")

        return flow_file.flows

    def _get_flows_from_path(
        self, flow_input: FlowDeployInput
    ) -> List[FlowDataFromFile]:
        if flow_input.file_path:
            flows_in_folder = self._flow_path_processing(flow_input.flow_path)
        elif flow_input.flow_data:
            flows_in_folder = self._blob_data_processing(flow_input.flow_data.blob)
        else:
            flows_in_folder = self.process_flows_folder()

        return flows_in_folder

    def _filter_flows_by_name(
        self,
        flows_in_folder: List[FlowDataFromFile],
        flow_name: str,
        flows_path: Optional[str],
    ) -> List[FlowDataFromFile]:
        flows_in_folder = [flow for flow in flows_in_folder if flow.name == flow_name]

        if len(flows_in_folder) == 0:
            if not flows_path:
                err_message = f"Flow with name '{flow_name}' was not found in flows home dir '{self.flows_home_path}'"
            else:
                err_message = (
                    f"Flow with name '{flow_name}' was not found in path '{flows_path}'"
                )
            raise FlowNotFound(err_message)
        return flows_in_folder

    def _clean_up_catalog_cache(self, flows_in_folder: List[FlowDataFromFile]) -> None:
        flow_names_in_folder = [flow.name for flow in flows_in_folder]

        clean_catalog = {
            flow_name: flow_data
            for flow_name, flow_data in self.catalog.items()
            if flow_name in flow_names_in_folder
        }
        self.catalog = clean_catalog

    def _get_version_from_tag(self, tags: List[str]) -> int:
        for tag in tags:
            if tag.startswith(cfg.VERSION_PREFIX):
                version = tag.split(cfg.TAG_DELIMITER)[1]
                return int(version)
        else:
            return 1

    def compare_cache_with_prefect(self):
        deployments_from_prefect = get_last_deployments_per_flow()
        flows_from_prefect = provider.get_flows()
        self.catalog = {}
        self.catalog_by_id = {}
        for flow_data in flows_from_prefect:
            _flow_data = flow_data.dict()
            last_flow_deployment = deployments_from_prefect.get(flow_data.id)
            if last_flow_deployment:
                _flow_data["deployment_id"] = last_flow_deployment.id
                _flow_data["deployment_name"] = last_flow_deployment.name
                _flow_data["version"] = self._get_version_from_tag(
                    last_flow_deployment.tags
                )
                flow = Flow(**_flow_data)
                self.catalog[_flow_data["name"]] = flow
                self.catalog_by_id[_flow_data["id"]] = flow
            else:
                logging.info(f"Flow without any deployment: {_flow_data['name']}")

    def register_and_deploy(
        self, flow_input: Optional[FlowDeployInput] = FlowDeployInput()
    ) -> List[Flow]:
        """
        flow_name - name of the Flow to deploy
        flow_path - path to the Flow to deploy

        if no flow_name & no flow_path - deploy all flows from the folder

        """
        logging.info("Checking for new flows or updates")

        # get flows from Prefect
        self.compare_cache_with_prefect()

        flows_updated = False

        flows_in_folder = self._get_flows_from_path(flow_input)

        if flow_input.name:
            flows_in_folder: List[FlowDataFromFile] = self._filter_flows_by_name(
                flows_in_folder, flow_input.name, flow_input.flow_path
            )

        flows_deployed = []

        for flow_file in flows_in_folder:
            # if it will be deploy with flow_name - in flows_in_folder will be only one flow with that name
            flow: Flow = self._process_flow_file_deployment(flow_file, flow_input.force)
            if flow:
                flows_deployed.append(flow)
                flows_updated = True

        if not flows_updated:
            logging.info("No new flows or updates was found")

        self.cache.write(self.catalog)
        return flows_deployed

    def _get_deployment_version(
        self, flow: Union[Flow, PrefectFlowResponse], flow_file: FlowDataFromFile
    ) -> int:
        if not isinstance(flow, PrefectFlowResponse):
            version = flow.version
            if flow.deployment_name != flow_file.deployment_name:
                # mean code was changed
                version += 1
        else:
            version = 1
        return version

    def _process_flow_file_deployment(
        self, flow_file: FlowDataFromFile, force: bool
    ) -> Optional[Flow]:

        flow: Union[Flow, PrefectFlowResponse] = self._prepare_flow_for_deployment(
            flow_file, force
        )

        if not flow:
            # mean no updates - no need to redeploy
            return
        version = self._get_deployment_version(flow, flow_file)
        full_flow_data = {}
        full_flow_data.update(flow.dict())
        full_flow_data.update(flow_file.dict())
        from pathlib import Path

        full_flow_data["flow_base_path"] = str(Path(full_flow_data["file_path"]).parent)
        flow_deploy_input = FlowDeployInput(**full_flow_data)
        deployment = self._deploy_flow(flow_deploy_input)

        flow = Flow(
            id=flow.id,
            name=flow_file.name,
            file_path=flow_file.file_path,
            deployment_id=deployment.id,
            deployment_name=deployment.name,
            version=version,
        )
        self.catalog[flow_file.name] = flow
        self.catalog_by_id[flow.id] = flow
        return flow

    def _prepare_flow_for_deployment(
        self, flow_file: FlowDataFromFile, force: bool
    ) -> Optional[PrefectFlowResponse]:
        if flow_file.name in self.catalog:
            if (
                flow_file.deployment_name
                and flow_file.file_modified
                == self.catalog[flow_file.name].deployment_name
            ) and not force:
                # no updates in file, no need to re-deploy
                return None
            logging.info(f"Deploying new version of flow '{flow_file.name}' in Prefect")
            flow = self.catalog[flow_file.name]
        else:
            logging.info(f"Registering new flow '{flow_file.name}' in Prefect")
            flow: PrefectFlowResponse = provider.create_flow(
                BaseFlowData(**flow_file.dict())
            )
        return flow

    def _deploy_flow(self, flow: FlowDeployInput) -> DeploymentResponse:
        deployment_response = create_flow_deployment(flow)
        return deployment_response

    def _get_full_flow_location(self, flow_file_name: str) -> str:
        return os.path.join(self.flows_home_path, flow_file_name)

    def process_flows_folder(self) -> List[FlowDataFromFile]:
        """list flows from FLOWS_HOME without register them or load them to Prefect if 'register' True"""

        flows_in_storage = self._get_storage().list()

        flows_in_folder = []

        for file_name in flows_in_storage:
            if not file_name.endswith(".py"):
                continue
            full_flow_path = self._get_full_flow_location(file_name)

            # get data from flow file
            flow_file = FlowFileReader(full_flow_path)
            flows_in_folder += flow_file.flows
        return flows_in_folder

    def list_flows(self) -> List[str]:
        return list(catalog.items())


catalog = Catalog.catalog
catalog_by_id = Catalog.catalog_by_id
