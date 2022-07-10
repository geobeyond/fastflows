import pytest
from fastapi.testclient import TestClient
from fastflows.schemas.flow import Flow
from fastflows.schemas.flow_run import FlowRunResponse


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
    print(create_flow.name)
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
    print(response_body)
    assert response.status_code == 200
