from fastapi.testclient import TestClient
from fastflows.schemas.flow import Flow


def test_flow_create(create_flow: Flow) -> None:
    assert create_flow.id is not None
    assert create_flow.deployment_id is not None


def test_flow_create_with_schedule(client: TestClient) -> None:
    flow_code = """
from time import sleep
from prefect import flow, task
import random


@task
def get_data():
    sleep(60)
    return random.randint(0, 100)


@flow(name="Flow from REST API")
def test_flow():
    get_data()


test_flow()
"""
    payload = {"flow_data": {"blob": flow_code}, "schedule": "0 5 * * *"}
    response = client.post("/flows", json=payload)
    response_body = response.json()[0]
    assert response.status_code == 200
    assert response_body["id"] is not None
    assert response_body["deployment_id"] is not None


def test_flow_create_by_flow_name_404(client: TestClient) -> None:

    payload = {"flow_name": "Simple Flow"}
    response = client.post("/flows", json=payload)
    response_body = response.json()
    assert response.status_code == 404
    assert (
        response_body["detail"]
        == "Flow with name 'Simple Flow' was not found in flows home dir 'tests/test_data/flows'"
    )


def test_flow_create_by_flow_name(client: TestClient) -> None:

    payload = {"flow_name": "Simple Flow2"}
    response = client.post("/flows", json=payload)
    response_body = response.json()[0]

    assert response.status_code == 200
    assert response_body["name"] == "Simple Flow2"
    assert response_body["id"]
    assert response_body["deployment_id"]


def test_flow_create_by_flow_path_404(client: TestClient) -> None:

    payload = {"flow_path": "Simple Flow2"}
    response = client.post("/flows", json=payload)
    response_body = response.json()

    assert response.status_code == 404
    assert (
        "Flow path 'tests/test_data/flows/Simple Flow2' does not"
        in response_body["detail"]
    )


def test_flow_create_by_flow_path(client: TestClient) -> None:

    payload = {"flow_path": "flow_with_params.py"}
    response = client.post("/flows", json=payload)
    response_body = response.json()[0]
    assert response.status_code == 200
    assert response_body["name"] == "Pipeline with Parameter"
    assert response_body["id"]
    assert response_body["deployment_id"]


def test_flow_deploy_all(client: TestClient) -> None:

    response = client.post("/flows", json={"force": True})
    response_body = response.json()
    assert response.status_code == 200
    assert len(response_body) == 2
    assert [flow["name"] for flow in response_body] == [
        "Pipeline with Parameter",
        "Simple Flow2",
    ]
