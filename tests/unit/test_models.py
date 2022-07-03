from fastflows.core.catalog import Catalog
from fastflows.providers.base import BaseProvider


def test_singletons_work_correctly():
    assert Catalog() != BaseProvider()
