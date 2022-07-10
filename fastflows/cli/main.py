import typer
from fastflows.main import app_run
from fastflows.cli.flows import flows_app
from fastflows.cli.flow_runs import flow_runs
from fastflows.cli.task_runs import task_runs
from fastflows.cli.utils import catch_exceptions


app = typer.Typer()


@app.command()
@catch_exceptions
def server():
    """Start FastFlows server"""
    typer.echo("Starting FastFlows server")
    app_run()


app.add_typer(
    flows_app, name="flows", help="Operate with Flows: get state, update state"
)
app.add_typer(
    flow_runs, name="flow-runs", help="Operate with Flow Runs: get state, update state"
)

app.add_typer(
    task_runs, name="task-runs", help="Operate with Tasks Runs: get state, update state"
)
