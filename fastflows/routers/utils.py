from functools import wraps
from fastflows.errors import FlowNotFound, FastFlowException, ApiValidationError
from fastapi import HTTPException
import pydantic


def handle_rest_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except FlowNotFound as e:
            raise HTTPException(status_code=404, detail=str(e))
        except (ApiValidationError, pydantic.error_wrappers.ValidationError) as e:
            raise HTTPException(status_code=422, detail=str(e))
        except FastFlowException as e:
            raise HTTPException(status_code=500, detail=str(e))

    return wrapper
