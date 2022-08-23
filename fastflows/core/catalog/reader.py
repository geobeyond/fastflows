import ast
import os
import sys
from fastflows.schemas.prefect.flow_data import (
    FlowDataFromFile,
    ScheduleFromFile,
    TagsFromFile,
    Schedule,
)
from typing import List, Optional, Tuple
from fastflows.config.app import configuration as cfg
from fastflows.core.utils.parse_data import parse_schedule_line, parse_tags_line


class FlowFileReader:
    def __init__(
        self, file_path: Optional[str] = None, flow_data: Optional[str] = None
    ) -> None:

        if not file_path and not flow_data:
            raise ValueError(
                "FlowFileReader expect one of 2 arguments: file_path or flow_data"
            )

        self.file_path = file_path
        self.file_data = flow_data or self._read_flow_file()
        # can be flow, but without name in decorator
        # todo: add test for both cases + case when there is no flow
        # can be several flows in one file
        self.flows: List[FlowDataFromFile] = []
        self._get_information_from_file()
        self.is_flows = bool(len(self.flows) > 0)

    def _read_flow_file(self) -> str:
        with open(self.file_path, "r") as f:
            return f.read()

    def _get_data_from_comment(self, key) -> Tuple[int, str]:
        for num, line in enumerate(self.file_data.split("\n")):
            line = line.strip()
            if line.startswith("#") and key in line:
                yield num, line.split(key)[1].replace(":", "", 1).strip()

    def _exctract_schedule_data(self):
        """expected comment in flow: `# schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC`"""
        schedules = []
        key = cfg.SCHEDULE_PROPERTY
        for num, line in self._get_data_from_comment(key):
            if line:
                schedule = parse_schedule_line(line)
                schedules.append(ScheduleFromFile(lineno=num, **schedule.dict()))

        return schedules

    def _exctract_tags(self):
        """expected comment in flow: `# tags: data_flow, some_tag`"""
        exctracted_tags = []
        key = cfg.TAGS_PROPERTY
        for num, line in self._get_data_from_comment(key):
            tags = parse_tags_line(line)
            if tags:
                exctracted_tags.append(TagsFromFile(lineno=num, tags=tags))
        return exctracted_tags

    def _get_information_from_file(self) -> None:
        parsed_ast = ast.parse(self.file_data)
        schedules: ScheduleFromFile = self._exctract_schedule_data()
        tags: TagsFromFile = self._exctract_tags()
        functions_in_file = [
            node
            for node in ast.walk(parsed_ast)
            if isinstance(node, ast.FunctionDef) and node.decorator_list
        ]

        # schedule should be written in comment with # before flow defenition

        for function in functions_in_file:
            self._process_function_node(function, schedules, tags)

    def _process_function_node(
        self,
        function: ast.FunctionDef,
        schedules: List[ScheduleFromFile],
        tags: List[TagsFromFile],
    ) -> None:
        decor = function.decorator_list[0]
        func_name = function.name
        flow_name = None
        is_flow = False
        if isinstance(decor, ast.Name) and decor.id == "flow":
            # mean no call, no args, no flow name, but it is a flow
            is_flow = True
        elif isinstance(decor, ast.Call) and decor.func.id == "flow":
            # mean it is call, so we have some args & kwargs
            is_flow = True
            for keyword in function.decorator_list[0].keywords:
                # 'name' can be passed only as keyword in flow
                if keyword.arg == "name":
                    if sys.version_info.minor >= 8:
                        flow_name = keyword.value.value
                    else:
                        flow_name = keyword.value.s

                    break
        if is_flow:
            schedule = [
                schedule for schedule in schedules if schedule.lineno < function.lineno
            ]
            if schedule:
                schedule = schedule[0]
                schedules.remove(schedule)
            else:
                schedule = None
            tag = [tag for tag in tags if tag.lineno < function.lineno]
            if tag:
                tag = tag[0]
                tags.remove(tag)

            flow = FlowDataFromFile(
                name=flow_name,
                entrypoint=f"{self.file_path}:{func_name}",
                file_path=self.file_path,
                file_modified=os.path.getmtime(self.file_path)
                if self.file_path
                else None,
                schedule=Schedule(**schedule.dict(exclude={"lineno"}))
                if schedule
                else None,
                tags=tag.tags if tag else [],
                flow_data=self.file_data,
            )
            self.flows.append(flow)
