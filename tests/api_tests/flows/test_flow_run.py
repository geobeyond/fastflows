from fastapi.testclient import TestClient
from fastflows.schemas.flow import Flow


def test_flow_run_by_id(create_flow: Flow, client: TestClient) -> None:
    response = client.post(f"/flows/{create_flow.id}")
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["flow_id"] == create_flow.id
    assert response_body["id"]
    assert response_body["state"]["type"] == "SCHEDULED"


def test_flow_run_by_name(create_flow: Flow, client: TestClient) -> None:
    response = client.post(f"/flows/name/{create_flow.name}")
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["flow_id"] == create_flow.id
    assert response_body["id"]
    assert response_body["state"]["type"] == "SCHEDULED"
