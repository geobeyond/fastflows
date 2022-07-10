import pytest
from typer.testing import CliRunner

from fastflows.cli.main import app
from fastflows.core.catalog import Catalog
from fastflows.config import app as cfg


flows_home_path = "tests/test_data/flows"


@pytest.fixture
def runner():
    return CliRunner()


cfg.configuration.FASTFLOW_DEBUG = 1
Catalog().set_flows_path(flows_home_path)


@pytest.fixture
def run_flow(runner: CliRunner):
    result = runner.invoke(
        app,
        ["flows", "run", "Simple Flow2"],
    )
    assert result.exit_code == 0
    assert "Run flow: Simple Flow2\nCreated flow run with id:" in result.stdout
    return result.stdout.split("id='")[1].split("'")[0]
