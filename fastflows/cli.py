import typer
import sys
from typing import List
from rich import print as rprint
from functools import wraps
import traceback
from typing import Optional
from fastflows.config.app import configuration
from fastflows.schemas.flow import FlowDeployInput
from fastflows.schemas.flow_run import FlowRunInput, StateBase, FlowRunStateEnum
from fastflows.schemas.deployment import DeploymentInputParams
from fastflows.main import app_run
from fastflows.core.flow_run import (
    update_flow_run_state,
    get_flow_run_details,
)
from fastflows.core.flow import (
    run_flow,
    list_flows_from_file_home,
    deploy_flows,
    get_flow_runs_list,
)
from fastflows.core.task_run import update_task_run_state, get_task_run_state

app = typer.Typer()


def catch_exceptions(func):
    """decorator to remove traceback in command line & convert output to red beutiful error message,
    to disable option & see traceback: set env FASTFLOW_DEBUG = 1
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if configuration.FASTFLOW_DEBUG == 1:
                typer.echo(traceback.format_exc())
            message = f"\n{e.args[0]}"
            typer.secho(message, fg=typer.colors.RED, err=True)
            sys.exit(1)

    return wrapper


@app.command()
@catch_exceptions
def server():
    """Start FastFlows server"""
    typer.echo("Starting FastFlows server")
    app_run()


# ---- Flow runs commands
flow_runs = typer.Typer()
app.add_typer(
    flow_runs, name="flow-runs", help="Operate with Flow Runs: get state, update state"
)


@flow_runs.command(name="list", help="List flow runs by flow_name or flow_id")
@catch_exceptions
def list_flow_runs(
    flow_name: str,
    flow_id: bool = typer.Option(False, help="List by flow_id"),
):
    typer.echo(
        f"Get list flow runs for flow {'with name' if not flow_id else 'with id'}: {flow_name}"
    )
    result = get_flow_runs_list(flow_name, flow_id)
    typer.echo(result)


@flow_runs.command(name="state", help="Get details for flow_run_id")
@catch_exceptions
def flow_run_state(flow_run_id: str):
    typer.echo(f"Get flow run state for flow_run_id {flow_run_id}")
    result = get_flow_run_details(flow_run_id)
    typer.echo(result)


@flow_runs.command(name="update", help="Update flow run state by flow_run_id")
@catch_exceptions
def update_flow_run(
    flow_run_id: str,
    state: str = typer.Option(
        FlowRunStateEnum.CANCELLED.value,
        help="State to set for new flow run - by default 'Scheduled' (mean will be runned imidiatly)",
    ),
):
    typer.echo(f"Set state {state} for flow_run_id {flow_run_id}")
    result = update_flow_run_state(flow_run_id, state=StateBase(type=state))
    typer.echo(result)


# ---- Flows commands
flows_app = typer.Typer()
app.add_typer(
    flows_app, name="flows", help="Operate with Flows: get state, update state"
)


def process_params_from_str(params: str) -> dict:
    params = params.strip().split()
    parameters = {}
    for pair in params:
        key, value = pair.split("=", 1)
        parameters[key] = value
    return parameters


@catch_exceptions
@flows_app.command(help="Run flow by Name or Id")
def run(
    flow_name: str,
    flow_id: bool = typer.Option(False, help="run by flow_id"),
    state: str = typer.Option(
        "PENDING",
        help="State to set for new flow run - by default 'Scheduled' (mean will be runned imidiatly)",
    ),
    params: Optional[str] = typer.Option(None, help="Parameters to pass to Flow Id"),
):
    typer.echo(f"Run flow: {flow_name}")
    if params:
        parameters = process_params_from_str(params)
    else:
        parameters = {}
    result = run_flow(
        flow_name,
        by_id=flow_id,
        flow_run_input=FlowRunInput(state={"type": state}, parameters=parameters),
    )
    typer.echo(f"Created flow run with id: {result.id}\n")
    typer.echo("Details:")
    rprint(result)


@flows_app.command()
@catch_exceptions
def list(flow_path: Optional[str] = configuration.FLOWS_HOME):
    """List all flows from FLOWS_HOME"""
    typer.echo("\nAll flows from FLOWS_HOME: \n")
    for flow in list_flows_from_file_home(flow_path):
        typer.echo(flow)
    typer.echo("\n")


@flows_app.command()
@catch_exceptions
def deploy(
    flows_home_path: str = typer.Argument(configuration.FLOWS_HOME),
    flow_name: Optional[str] = typer.Option(None, help="Flow name to deploy"),
    flow_path: Optional[str] = typer.Option(None, help="Flow path to deploy"),
    schedule: Optional[str] = typer.Option(
        None,
        help="""Schedule that should be used in the Deployment. If it will be used without `flow_path` or `flow_name` options
        this mean that ALL flows from path will be deployed with that schedule.""",
    ),
    active: Optional[bool] = typer.Option(True, help="Activate flow after deploy"),
    tags: Optional[List[str]] = typer.Option(None, help="Tags for deployment"),
    params: Optional[str] = typer.Option(None, help="Parameters for deployment"),
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
        typer.echo(f"Deploy all flows from path: {flow_path}")

    deploy_flows(
        flow_input=FlowDeployInput(
            flows_home_path=flows_home_path,
            flow_name=flow_name,
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


# ---- Task Runs Comands
task_runs = typer.Typer()
app.add_typer(
    task_runs, name="task-runs", help="Operate with Tasks Runs: get state, update state"
)


@task_runs.command(name="update")
@catch_exceptions
def update_task_runs(task_run_id: str):
    typer.echo(f"Update task with id: {task_run_id}")
    update_task_run_state(task_run_id)


@task_runs.command(name="state")
@catch_exceptions
def task_run_state(task_run_id: str):
    typer.echo(f"Get state for task run task with id: {task_run_id}")
    get_task_run_state(task_run_id)
