""" flows command """
import typing
from pathlib import Path

import typer
from rich import print as rprint

from ..config import settings
from ..schemas.prefect.flow import FlowDeployInput
from ..schemas.prefect.flow_run import FlowRunInput
from ..schemas.prefect.deployment import DeploymentInputParams
from ..core.utils import parse_data
from ..core import flow as flow_ops
from ..utils.core import (
    check_path_is_dir,
    check_path_exists,
)
from . import utils

flows_app = typer.Typer()

params_doc_string = 'Can be passed as a comma separated string like \'key1=value1,key2=value2\'. Or as a json like {"a": "b"}'


@utils.catch_exceptions
@flows_app.command(help="Run flow by Name or Id")
def run(
    flow_name: str,
    flow_id: bool = typer.Option(False, help="run by flow_id"),
    state: str = typer.Option(
        "SCHEDULED",
        callback=lambda v: v.upper(),
        help="State to set for new flow run - by default 'Scheduled' (mean that Flow will be runned imidiatly)",
    ),
    params: typing.Optional[str] = typer.Option(
        None,
        callback=utils.process_params_from_str,
        help=f"Parameters to pass to Flow Id. {params_doc_string}",
    ),
):
    typer.echo(f"Run flow: {flow_name}")
    result = flow_ops.run_flow(
        flow_name,
        by_id=flow_id,
        flow_run_input=FlowRunInput(state={"type": state}, parameters=params),
    )
    typer.echo(f"Created flow run with id: {result.id}\n")
    typer.echo("Details:")
    rprint(result)


@flows_app.command()
@utils.catch_exceptions
def list(flow_path: typing.Optional[Path] = settings.FLOWS_HOME):
    """List all flows from FLOWS_HOME"""
    typer.echo("\nAll flows from FLOWS_HOME: \n")
    typer.echo(f"\nAvailable flows: {flow_ops.list_flows(flows_home_path=flow_path)}\n")


@flows_app.command()
@utils.catch_exceptions
def deploy(
    flows_home_path: Path = typer.Argument(
        settings.FLOWS_HOME, callback=check_path_is_dir
    ),
    flow_name: typing.Optional[str] = typer.Option(None, help="Flow name to deploy"),
    flow_path: typing.Optional[Path] = typer.Option(
        None, help="Flow path to deploy", callback=check_path_exists
    ),
    schedule: typing.Optional[str] = typer.Option(
        None,
        callback=parse_data.parse_schedule_line,
        help="""Schedule that should be used in the Deployment. If it will be used without `flow_path` or `flow_name` options
        this mean that ALL flows from path will be deployed with that schedule.
        Example of schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC""",
    ),
    active: typing.Optional[bool] = typer.Option(
        True, help="Activate flow after deploy"
    ),
    tags: typing.Optional[typing.List[str]] = typer.Option(
        None, callback=parse_data.parse_tags_line, help="Tags for deployment"
    ),
    params: typing.Optional[str] = typer.Option(
        None, help=f"Parameters for deployment. {params_doc_string}"
    ),
    force: bool = typer.Option(False, help="Force re-deploy all flows"),
):
    """Register flows in FastFlows & Prefect server"""

    if not flow_path:
        sub_message = f"from directory: {flows_home_path.as_posix()}"
    else:
        sub_message = f"from path: {flow_path.as_posix()}"
    if flow_name:
        main_message = f"Deploy flow '{flow_name}'"
    else:
        main_message = "Deploy all flows"

    typer.echo(f"{main_message} {sub_message}")

    flow_ops.deploy_flows(
        flow_input=FlowDeployInput(
            flows_home_path=flows_home_path,
            name=flow_name,
            file_path=flow_path,
            deployment_params=DeploymentInputParams(
                schedule=schedule,
                is_schedule_active=active,
                parameters=params,
                tags=tags,
            ),
            force=force,
        )
    )
