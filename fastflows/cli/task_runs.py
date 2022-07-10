import typer
from fastflows.core.task_run import update_task_run_state, get_task_run_state
from fastflows.cli.utils import catch_exceptions


# ---- Task Runs Comands
task_runs = typer.Typer()


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
