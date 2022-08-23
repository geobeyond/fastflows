""" flows command """
import typer
from typing import List
from rich import print as rprint
from typing import Optional
from fastflows.config.app import configuration
from fastflows.schemas.prefect.flow import FlowDeployInput
from fastflows.schemas.prefect.flow_run import FlowRunInput
from fastflows.schemas.prefect.deployment import DeploymentInputParams
from fastflows.core.utils.parse_data import parse_schedule_line, parse_tags_line
from fastflows.core.flow import run_flow, list_flows, deploy_flows
from fastflows.cli.utils import (
    catch_exceptions,
    process_params_from_str,
    check_path_is_dir,
    check_path_exists,
)


flows_app = typer.Typer()

params_doc_string = 'Can be passed as a comma separated string like \'key1=value1,key2=value2\'. Or as a json like {"a": "b"}'


@catch_exceptions
@flows_app.command(help="Run flow by Name or Id")
def run(
    flow_name: str,
    flow_id: bool = typer.Option(False, help="run by flow_id"),
    state: str = typer.Option(
        "SCHEDULED",
        callback=lambda v: v.upper(),
        help="State to set for new flow run - by default 'Scheduled' (mean that Flow will be runned imidiatly)",
    ),
    params: Optional[str] = typer.Option(
        None,
        callback=process_params_from_str,
        help=f"Parameters to pass to Flow Id. {params_doc_string}",
    ),
):
    typer.echo(f"Run flow: {flow_name}")
    result = run_flow(
        flow_name,
        by_id=flow_id,
        flow_run_input=FlowRunInput(state={"type": state}, parameters=params),
    )
    typer.echo(f"Created flow run with id: {result.id}\n")
    typer.echo("Details:")
    rprint(result)


@flows_app.command()
@catch_exceptions
def list(flow_path: Optional[str] = configuration.FLOWS_HOME):
    """List all flows from FLOWS_HOME"""
    typer.echo("\nAll flows from FLOWS_HOME: \n")
    typer.echo(f"\nAvailable flows: {list_flows(flows_home_path=flow_path)}\n")


@flows_app.command()
# @catch_exceptions
def deploy(
    flows_home_path: str = typer.Argument(
        configuration.FLOWS_HOME, callback=check_path_is_dir
    ),
    flow_name: Optional[str] = typer.Option(None, help="Flow name to deploy"),
    flow_path: Optional[str] = typer.Option(
        None, help="Flow path to deploy", callback=check_path_exists
    ),
    schedule: Optional[str] = typer.Option(
        None,
        callback=parse_schedule_line,
        help="""Schedule that should be used in the Deployment. If it will be used without `flow_path` or `flow_name` options
        this mean that ALL flows from path will be deployed with that schedule.
        Example of schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC""",
    ),
    active: Optional[bool] = typer.Option(True, help="Activate flow after deploy"),
    tags: Optional[List[str]] = typer.Option(
        None, callback=parse_tags_line, help="Tags for deployment"
    ),
    params: Optional[str] = typer.Option(
        None, help=f"Parameters for deployment. {params_doc_string}"
    ),
    force: bool = typer.Option(False, help="Force re-deploy all flows"),
):
    """Register flows in FastFlows & Prefect server"""
    if flow_name:
        if not flow_path:
            sub_message = f"from directory: {flows_home_path}"
        else:
            sub_message = f"from path: {flow_path}"
        typer.echo(f"Deploy flow '{flow_name}' {sub_message}")

    else:
        typer.echo(f"Deploy all flows from path: {flows_home_path}")

    deploy_flows(
        flow_input=FlowDeployInput(
            flows_home_path=flows_home_path,
            name=flow_name,
            flow_path=flow_path,
            deployment_params=DeploymentInputParams(
                schedule=schedule,
                is_schedule_active=active,
                parameters=params,
                tags=tags,
            ),
            force=force,
        )
    )
