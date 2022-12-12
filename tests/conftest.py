import pathlib
import pytest
from fastflows.core.catalog import Catalog

flows_home_path = pathlib.Path("tests/test_data/flows")

Catalog().set_flows_path(flows_home_path)


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: run only unit tests")


@pytest.fixture
def flows_folder() -> str:
    current_folder = pathlib.Path(__file__).parent
    return str(current_folder / "test_data" / "flows")
