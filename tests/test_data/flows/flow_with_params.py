# schedule: interval=3600,anchor_date=2020-01-01T00:00:00Z,timezone=UTC
# tags: data_flow, some_tag
from prefect import task, flow, get_run_logger


@task
def deploy(name):
    logger = get_run_logger()
    logger.info(f"Name: {name}")


@flow(name="Params Flow")
def github_stars(name):
    deploy(name)
