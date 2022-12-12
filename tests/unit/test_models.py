import pytest

from fastflows.core.catalog import Catalog
from fastflows.providers.base import BaseProvider

pytestmark = pytest.mark.unit


def test_singletons_work_correctly():
    assert Catalog() != BaseProvider()
