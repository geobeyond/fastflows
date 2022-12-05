import pytest
from typer.testing import CliRunner

from fastflows.cli.main import app
from fastflows.config import app as cfg


@pytest.fixture
def runner():
    return CliRunner()


cfg.settings.DEBUG = True


@pytest.fixture
def run_flow(runner: CliRunner):
    result = runner.invoke(
        app,
        ["flows", "run", "Simple Flow2"],
    )
    assert result.exit_code == 0
    assert "Created flow run with id:" in result.stdout
    return result.stdout.split("id='")[1].split("'")[0]


@pytest.fixture
def run_flow_with_subflow(runner: CliRunner):
    result = runner.invoke(
        app,
        ["flows", "run", "With Subflow", "--params", "name=name"],
    )
    assert result.exit_code == 0
    assert "Created flow run with id:" in result.stdout
    return result.stdout.split("id='")[1].split("'")[0]
