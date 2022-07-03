from time import sleep
from prefect import flow, task
import random


@task
def get_data():
    sleep(60)
    return random.randint(0, 100)


@flow(name="Simple Flow2")
def test_flow():
    get_data()


test_flow()
