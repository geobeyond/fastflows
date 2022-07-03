from pydantic import BaseModel


class FastFlowException(Exception):
    def __init__(self, message: str = "Error while processing request"):

        super().__init__(message)


class FlowNotFound(FastFlowException):
    def __init__(self, message: str = "Flow was not found"):
        super().__init__(message)


def api_response_handler(response_model: BaseModel, message: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
                if response.status_code != 200:
                    response = response.json()
                    return response_model(**response)
                else:
                    raise FastFlowException()
                return func(*args, **kwargs)
            except Exception as e:
                raise FastFlowException(message) from e

        return wrapper

    return decorator
