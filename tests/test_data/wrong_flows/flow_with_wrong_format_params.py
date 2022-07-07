# schedule: 0 0 * * *
from time import sleep
from prefect import task, flow


@task
def one():
    sleep(20)


@task
def deploy(name):
    """With the manual_only trigger this task will only run after it has been approved"""
    print(f"Name: {name}")


@flow(name="Pipeline with Parameter")
def github_stars(name):
    deploy(name, upstream_tasks=[one])
