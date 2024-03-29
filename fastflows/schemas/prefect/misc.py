import datetime
from pydantic import BaseModel
from typing import Optional
from enum import Enum
import hashlib


class DefaultAPIResponseModel(BaseModel):
    status = "success"


class Schedule(BaseModel):

    interval: int
    timezone: str = "UTC"
    anchor_date: datetime.datetime


def get_hash_from_data(data: str) -> str:
    # The following line is being marked with noqa because
    # 'Consider usedforsecurity=False' not being used because it does not exist
    # in Python 3.8
    return hashlib.md5(data.encode()).hexdigest()  # noqa: S324


class Status(str, Enum):
    ACCEPT = "ACCEPT"
    ABORT = "ABORT"


class Details(BaseModel):
    type: str
    reason: Optional[str]
