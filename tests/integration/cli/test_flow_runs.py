from typer.testing import CliRunner
from tests.integration.cli.conftest import app
from fastflows.schemas.flow import Flow


def test_change_state_flow_run_error(runner: CliRunner, run_flow: Flow):
    result = runner.invoke(
        app,
        ["flow-runs", "update", run_flow],
    )
    assert result.exit_code == 1
    assert "You should provide state to set to Flow Run" in result.stdout


def test_change_state_flow_run_ok(runner: CliRunner, run_flow: Flow):
    result = runner.invoke(
        app,
        ["flow-runs", "update", run_flow, "--state", "CANCELLED"],
    )
    assert result.exit_code == 0
    assert "Set state CANCELLED for flow_run_id" in result.stdout
    assert "status=<Status.ACCEPT: 'ACCEPT'>" in result.stdout


def test_cancel_flow_run(runner: CliRunner, run_flow: Flow):
    result = runner.invoke(
        app,
        ["flow-runs", "cancel", run_flow],
    )
    assert result.exit_code == 0
    assert "Cancel flow run with flow_run_id " in result.stdout


def test_flow_run_with_sub_flow_and_graph_option(
    runner: CliRunner, run_flow_with_subflow: Flow
):
    result = runner.invoke(
        app,
        ["flow-runs", "details", run_flow_with_subflow, "--graph"],
    )
    assert result.exit_code == 0
    assert "Get graph for flow_run_id" in result.stdout
