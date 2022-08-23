from typing import Optional, _GenericAlias, Callable
from pydantic import BaseModel
import fastflows
import httpx
from fastflows import errors
from fastflows.schemas.prefect.misc import DefaultAPIResponseModel


def get_response_model(func: Callable, response_model: Optional[BaseModel]):

    if not response_model:
        if func.__annotations__.get("return"):
            if func.__annotations__["return"] == str:
                return None
            return func.__annotations__["return"]
        else:
            return DefaultAPIResponseModel
    else:
        _response_model = response_model

        if isinstance(_response_model, _GenericAlias):
            _response_model = _response_model.__args__[0]

        return _response_model


def api_response_handler(
    response_model: Optional[BaseModel] = None,
    message: str = "Some unexpected error occures during the API call",
    args_in_message: bool = False,
    append_api_error: bool = True,
):
    def decorator(func):
        _response_model = get_response_model(func, response_model)

        def wrapper(*args, **kwargs):
            try:
                response = func(*args, **kwargs)
            except httpx.ConnectError as e:
                raise fastflows.errors.FastFlowException(
                    f"Problems with resolving Prefect host: {str(e)}."
                )
            status_code_check = str(response.status_code).startswith
            if status_code_check("2"):
                response = response.json()
                if _response_model:
                    if isinstance(response, list):
                        processed_response = []
                        for item in response:
                            processed_response.append(_response_model(**item))
                    else:
                        processed_response = _response_model(**response)
                    return processed_response
                else:
                    return response
            else:
                if response.status_code == 422:
                    raise errors.ApiValidationError(response.json())
                raise fastflows.errors.FastFlowException(
                    f"Error API response: {response.text}. Status code: {response.status_code}"
                )

        return wrapper

    return decorator
