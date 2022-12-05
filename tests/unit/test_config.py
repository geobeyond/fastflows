import os
from unittest import mock
import importlib


@mock.patch.dict(
    os.environ,
    {
        "ENV_NAME": "dev",
        "dev__FASTFLOWS__PREFECT__URI": "http://dev-test-url",
    },
)
def test_define_config_based_ENV_NAME():

    from fastflows.config import app

    importlib.reload(app)

    FastFlowsSettings = app.FastFlowsSettings
    assert FastFlowsSettings().PREFECT.URI == "http://dev-test-url"


@mock.patch.dict(
    os.environ,
    {
        "ENV_NAME": "ANY",
        "ANY__FASTFLOWS__PREFECT__URI": "http://ANY-test-url",
    },
)
def test_define_config_based_ENV_NAME_2():

    from fastflows.config import app

    importlib.reload(app)

    FastFlowsSettings = app.FastFlowsSettings
    assert FastFlowsSettings().PREFECT.URI == "http://ANY-test-url"
