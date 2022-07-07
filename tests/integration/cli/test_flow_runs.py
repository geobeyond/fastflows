from typer.testing import CliRunner
from tests.integration.cli.conftest import app
from fastflows.schemas.flow import Flow


def test_change_state_flow_run(runner: CliRunner, run_flow: Flow):
    result = runner.invoke(
        app,
        ["flow-runs", "update", run_flow],
    )
    assert result.exit_code == 0
    assert "Set state CANCELLED for flow_run_id" in result.stdout
    assert "status=<Status.ACCEPT: 'ACCEPT'>" in result.stdout
