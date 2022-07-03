import os
from unittest import mock
import importlib


@mock.patch.dict(
    os.environ,
    {
        "ENV_NAME": "dev",
        "dev_PREFECT_URI": "http://dev-test-url",
    },
)
def test_define_config_based_ENV_NAME():

    from fastflows.config import app

    importlib.reload(app)

    Config = app.Config
    assert Config().ENV_NAME == "dev"
    assert Config().PREFECT_URI == "http://dev-test-url"


@mock.patch.dict(
    os.environ,
    {
        "ENV_NAME": "ANY",
        "ANY_PREFECT_URI": "http://ANY-test-url",
    },
)
def test_define_config_based_ENV_NAME_2():

    from fastflows.config import app

    importlib.reload(app)

    Config = app.Config
    assert Config().ENV_NAME == "ANY"
    assert Config().PREFECT_URI == "http://ANY-test-url"
