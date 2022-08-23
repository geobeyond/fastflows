from fastflows.schemas.prefect.task_run import TaskRunState, TaskState


def update_task_run_state(task_run_id: str):
    # call provider API
    return TaskRunState(id=task_run_id, state=TaskState.MAPPED)


def get_task_run_state(task_run_id: str):
    pass
