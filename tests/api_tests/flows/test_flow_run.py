import pytest
from fastapi.testclient import TestClient
from fastflows.schemas.prefect.flow import Flow
from fastflows.schemas.prefect.flow_run import FlowRunResponse


@pytest.fixture
def flow_run(create_flow: Flow, client: TestClient) -> FlowRunResponse:
    response = client.post(f"/flows/{create_flow.id}")
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["flow_id"] == create_flow.id
    assert response_body["id"]
    assert response_body["state"]["type"] == "SCHEDULED"
    return FlowRunResponse(**response_body)


def test_flow_run_by_id(flow_run: FlowRunResponse) -> None:
    assert flow_run.id


def test_flow_run_by_name(create_flow: Flow, client: TestClient) -> None:
    response = client.post(f"/flows/name/{create_flow.name}")
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["flow_id"] == create_flow.id
    assert response_body["id"]
    assert response_body["state"]["type"] == "SCHEDULED"


def test_update_flow_run_state(flow_run: FlowRunResponse, client: TestClient) -> None:
    response = client.patch(
        f"/flow-runs/{flow_run.id}/state", json={"type": "CANCELLED"}
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["status"] == "ACCEPT"


def test_flow_run_by_id_not_exists(client: TestClient) -> None:
    response = client.post("/flows/any-id-not-exists")
    response_body = response.json()
    assert response.status_code == 404
    assert "Flow was not found in Catalog. Available flows" in response_body["detail"]


def test_flow_run_by_name_not_exists(client: TestClient) -> None:
    response = client.post("/flows/name/any-id-not-exists")
    response_body = response.json()
    assert response.status_code == 404
    assert "Flow was not found in Catalog. Available flows" in response_body["detail"]


def test_update_flow_run_state_422(client: TestClient) -> None:
    response = client.patch("/flow-runs/not-id/state", json={"type": "CANCELLED"})
    response_body = response.json()
    assert response.status_code == 422
    assert "value is not a valid uui" in response_body["detail"]


def test_flow_run_by_name_with_params(client: TestClient) -> None:
    response = client.post(
        "/flows/name/Params Flow", json={"parameters": {"name": "value1"}}
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["id"]
    assert response_body["parameters"] == {"name": "value1"}


def test_get_flow_run_graph(flow_run: FlowRunResponse, client: TestClient) -> None:
    response = client.get(f"/flow-runs/{flow_run.id}/graph")
    response_body = response.json()
    assert response.status_code == 200
    # need to wait to complete flow for graph to be generated
    assert response_body == []


def test_flow_run_by_name_with_params_file_path(client: TestClient) -> None:
    params = {"path_to_file": "test.txt"}
    response = client.post("/flows/name/file_reader", json={"parameters": params})
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["id"]
    assert response_body["parameters"] == params
    assert response_body["state"]["type"] == "SCHEDULED"
