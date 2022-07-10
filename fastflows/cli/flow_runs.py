import typer
from fastflows.schemas.flow_run import StateBase, FlowRunStateEnum
from fastflows.core.flow_run import (
    update_flow_run_state,
    get_flow_run_details,
)
from fastflows.core.flow import (
    get_flow_runs_list,
)
from fastflows.cli.utils import catch_exceptions

# ---- Flow runs commands
flow_runs = typer.Typer()


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
        callback=lambda v: v.upper(),
        help="State to set for new flow run - by default 'Scheduled' (mean will be runned imidiatly)",
    ),
):
    typer.echo(f"Set state {state} for flow_run_id {flow_run_id}")
    result = update_flow_run_state(flow_run_id, state=StateBase(type=state))
    typer.echo(result)
