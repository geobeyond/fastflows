import pathlib
import pytest


@pytest.fixture
def flows_folder() -> str:
    current_folder = pathlib.Path(__file__).parent
    return str(current_folder / "test_data" / "flows")
