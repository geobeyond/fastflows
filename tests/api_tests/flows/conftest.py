import pytest
from fastapi.testclient import TestClient
from fastflows.main import app
from fastflows.schemas.prefect.flow import Flow

import logging

logging.getLogger("botocore").setLevel(logging.CRITICAL)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def create_flow(client: TestClient) -> Flow:
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
    payload = {"flow_data": flow_code}
    response = client.post("/flows", json=payload)
    response_body = response.json()

    return [Flow(**flow) for flow in response_body][0]
