import datetime
from pydantic import BaseModel

import hashlib


class DefaultAPIResponseModel(BaseModel):
    status = "success"


class Schedule(BaseModel):

    interval: int
    timezone: str = "UTC"
    anchor_date: datetime.datetime


def get_hash_from_data(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()
