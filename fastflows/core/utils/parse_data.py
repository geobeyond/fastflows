from fastflows.errors import FastFlowException
from fastflows.schemas.prefect.flow_data import Schedule
import pydantic
from typing import List, Optional


def parse_schedule_line(line: Optional[str]) -> Optional[Schedule]:
    if line:
        data = [item.strip() for item in line.split(",")]
        schedule_data = {}
        for item in data:
            item = item.split("=")
            if item[0] in Schedule.__fields__:
                schedule_data[item[0]] = item[1]
        try:
            return Schedule(**schedule_data)
        except pydantic.error_wrappers.ValidationError:
            raise FastFlowException(
                "Wrong schedule format."
                "Schedule in Flow File should be defined as comment line with interval & anchor_date & timezone"
                "Example: `# schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC`"
            )


def parse_tags_line(line: Optional[str]) -> List[str]:
    if line:
        tags = [item.strip() for item in line.split(",")]
        if tags:
            return tags
    return []
