import pytest
from typer.testing import CliRunner
from tests.conftest import flows_home_path
from tests.integration.cli.conftest import app


# todo: need to mock prefect to run it on CI
def test_flows_not_existed_flow(runner: CliRunner):
    result = runner.invoke(app, 'flows deploy --flow-name "simple"'.split())
    assert result.exit_code == 1
    assert (
        "Flow with name '\"simple\"' was not found in flows home dir" in result.stdout
    )


def test_flows_existed_flow(runner: CliRunner):
    result = runner.invoke(
        app,
        ["flows", "deploy", flows_home_path.as_posix(), "--flow-name", "Simple Flow2"],
    )
    assert result.exit_code == 0
    assert (
        "Deploy flow 'Simple Flow2' from directory: tests/test_data/flows"
        in result.stdout
    )


def test_flows_existed_flow_path(runner: CliRunner):
    result = runner.invoke(
        app,
        ["flows", "deploy", "--flow-path", "tests/test_data/flows/flow_with_params.py"],
    )
    assert result.exit_code == 0
    assert (
        "Deploy all flows from path: tests/test_data/flows/flow_with_params.py"
        in result.stdout
    )


def test_flows_existed_flow_path_with_flow_name_err(runner: CliRunner):
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
    assert result.exit_code == 1

    assert (
        "Flow with name 'Simple Flow2' was not found in path 'tests/test_data/flows/flow_with_params.py'"
        in result.stdout
    )


def test_flows_existed_flow_path_with_flow_name(runner: CliRunner):
    result = runner.invoke(
        app,
        [
            "flows",
            "deploy",
            "--flow-path",
            "tests/test_data/flows/flow_with_params.py",
            "--flow-name",
            "Params Flow",
        ],
    )
    assert result.exit_code == 0
    assert (
        "Deploy flow 'Params Flow' from path: tests/test_data/flows/flow_with_params.py"
        in result.stdout
    )


@pytest.mark.skip(reason="fix later")
def test_flows_existed_flow_path_with_flow_name_wrong_params_format(runner: CliRunner):
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
    assert result.exit_code == 1
    assert (
        "Deploy flow 'Pipeline with Parameter' from path: tests/test_data/flows/flow_with_params.py"
        in result.stdout
    )


def test_create_flow_run(run_flow: str) -> None:
    assert run_flow is not None


def test_flows_list(runner: CliRunner):
    result = runner.invoke(
        app,
        ["flows", "list"],
    )
    assert result.exit_code == 0
    assert "Available flows: " in result.stdout


def test_flows_run_with_params(runner: CliRunner):
    result = runner.invoke(
        app,
        [
            "flows",
            "run",
            "Params Flow",
            "--params",
            '{"name": "some-name-from-params"}',
        ],
    )
    assert result.exit_code == 0
    assert "parameters={'name': 'some-name-from-params'}" in result.stdout
