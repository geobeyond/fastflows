import pytest
from typer.testing import CliRunner

from fastflows.cli import app
from fastflows.core.catalog import Catalog
from fastflows.config import app as cfg

runner = CliRunner()

cfg.configuration.FASTFLOW_DEBUG = 1
flows_home_path = "tests/test_data/flows"
Catalog().set_flows_path(flows_home_path)


def test_flows_not_existed_flow():
    result = runner.invoke(app, 'flows deploy --flow-name "simple"'.split())
    assert result.exit_code == 1
    assert (
        "Flow with name '\"simple\"' was not found in flows home dir" in result.stdout
    )


def test_flows_existed_flow():
    result = runner.invoke(
        app, ["flows", "deploy", flows_home_path, "--flow-name", "Simple Flow2"]
    )
    assert result.exit_code == 0
    assert (
        "Deploy flow 'Simple Flow2' from directory: tests/test_data/flows"
        in result.stdout
    )


def test_flows_existed_flow_path():
    result = runner.invoke(
        app,
        ["flows", "deploy", "--flow-path", "tests/test_data/flows/flow_with_params.py"],
    )
    assert result.exit_code == 0
    assert (
        "Deploy all flows from path: tests/test_data/flows/flow_with_params.py"
        in result.stdout
    )


def test_flows_existed_flow_path_with_flow_name_err():
    result = runner.invoke(
        app,
        [
            "flows",
            "deploy",
            "--flow-path",
            "tests/test_data/flows/flow_with_params.py",
            "--flow-name",
            "Simple Flow2",
        ],
    )
    print(result.stdout)
    assert result.exit_code == 1
    assert (
        "Flow with name 'Simple Flow2' was not found in path 'tests/test_data/flows/flow_with_params.py'"
        in result.stdout
    )


def test_flows_existed_flow_path_with_flow_name():
    result = runner.invoke(
        app,
        [
            "flows",
            "deploy",
            "--flow-path",
            "tests/test_data/flows/flow_with_params.py",
            "--flow-name",
            "Pipeline with Parameter",
        ],
    )
    print(result.stdout)
    assert result.exit_code == 0
    assert (
        "Deploy flow 'Pipeline with Parameter' from path: tests/test_data/flows/flow_with_params.py"
        in result.stdout
    )


@pytest.mark.skip(reason="fix later")
def test_flows_existed_flow_path_with_flow_name_wrong_params_format():
    result = runner.invoke(
        app,
        [
            "flows",
            "deploy",
            "--flow-path",
            "tests/test_data/wrong_flows/flow_with_wrong_format_params.py",
            "--flow-name",
            "Pipeline with Parameter",
        ],
    )
    print(result.stdout)
    assert result.exit_code == 1
    assert (
        "Deploy flow 'Pipeline with Parameter' from path: tests/test_data/flows/flow_with_params.py"
        in result.stdout
    )
