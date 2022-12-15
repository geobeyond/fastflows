from functools import wraps
from fastflows.errors import FlowNotFoundError, FastFlowsError, ApiValidationError
from fastapi import HTTPException
import pydantic


def handle_rest_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FlowNotFoundError as e:
            raise HTTPException(status_code=404, detail=str(e)) from e
        except (ApiValidationError, pydantic.error_wrappers.ValidationError) as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except FastFlowsError as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    return wrapper
