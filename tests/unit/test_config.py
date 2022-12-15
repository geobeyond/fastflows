import importlib
from unittest import mock

import pytest

# NOTE: do not modify the below import line - There are tests below that use importlib to reload the `config` module
from fastflows import config

pytestmark = pytest.mark.unit


@pytest.mark.parametrize(
    "env_key, env_value, setting_key, expected",
    [
        pytest.param("DEBUG", "true", "DEBUG", True),
        pytest.param("DEBUG", "false", "DEBUG", False),
        pytest.param(
            "PREFECT__URI",
            "http://dev0-test-url",
            "PREFECT.URI",
            "http://dev0-test-url",
        ),
        pytest.param(
            "PREFECT__STORAGE__BLOCK_TYPE",
            "local-file-system",
            "PREFECT.STORAGE.BLOCK_TYPE",
            "local-file-system",
        ),
    ],
)
def test_define_config_no_env_name(env_key, env_value, setting_key, expected):
    with mock.patch.dict("os.environ", {env_key: env_value}, clear=True):
        settings = config.FastFlowsSettings()  # noqa
        got = eval(f"settings.{setting_key}")  # noqa
        assert got == expected


@pytest.mark.parametrize(
    "env_name_value, env_key, env_value, setting_key, expected",
    [
        pytest.param("", "DEBUG", "true", "DEBUG", True),
        pytest.param("dev__", "dev__DEBUG", "true", "DEBUG", True),
        pytest.param(
            "",
            "PREFECT__URI",
            "http://dev1-test-url",
            "PREFECT.URI",
            "http://dev1-test-url",
        ),
        pytest.param(
            "any",
            "anyPREFECT__URI",
            "http://dev1-test-url",
            "PREFECT.URI",
            "http://dev1-test-url",
        ),
        pytest.param(
            "dev__",
            "dev__PREFECT__URI",
            "http://dev1-test-url",
            "PREFECT.URI",
            "http://dev1-test-url",
        ),
    ],
)
def test_define_config_based_env_name(
    env_name_value: str, env_key: str, env_value: str, setting_key: str, expected
):
    with mock.patch.dict(
        "os.environ",
        {
            "ENV_NAME": env_name_value,
            env_key: env_value,
        },
        clear=True,
    ):
        # we reload the `config` module here in order to have the custom logic that is
        # associated with the ENV_NAME environment variable be re-triggered - such logic
        # is executed at import time
        importlib.reload(config)
        settings = config.FastFlowsSettings()  # noqa
        got = eval(f"settings.{setting_key}")  # noqa
        assert got == expected
