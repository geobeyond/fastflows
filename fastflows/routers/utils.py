from functools import wraps
from fastflows.errors import FlowNotFound
from fastapi import HTTPException


def handle_rest_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FlowNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))

    return wrapper
