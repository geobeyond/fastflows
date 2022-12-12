import os
import datetime

import pytest

from fastflows.core.catalog.reader import FlowFileReader

pytestmark = pytest.mark.unit


def test_extract_tags(flows_folder):
    file_reader = FlowFileReader(file_path=os.path.join(flows_folder, "simple_flow.py"))
    file_reader.file_data = "# tags: data_flow, some_tag"
    assert file_reader._exctract_tags()[0].tags == ["data_flow", "some_tag"]


def test_extract_schedule(flows_folder):
    file_reader = FlowFileReader(file_path=os.path.join(flows_folder, "simple_flow.py"))
    file_reader.file_data = (
        "# schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC"
    )
    assert file_reader._exctract_schedule_data()[0].dict() == {
        "anchor_date": datetime.datetime(
            2020, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
        ),
        "interval": 3600,
        "lineno": 0,
        "timezone": "UTC",
    }
