# schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC
# tags: sub_flow, some_tag
from prefect import task, flow, get_run_logger
import uuid


@task
def deploy(name):
    logger = get_run_logger()
    logger.info(f"Name: {name}")
    return name + uuid.uuid1().hex


@flow(name="With Subflow")
def github_stars(name):

    hex_name = deploy(name)
    my_subflow(hex_name)

    return {"some-data": "Magic flow Data"}


@flow(name="Subflow")
def my_subflow(hex_name):
    logger = get_run_logger()
    logger.info(f"Subflow says: {hex_name}")
