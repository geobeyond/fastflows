# schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC
# tags: data_flow, some_tag
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
