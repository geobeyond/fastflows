import logging
from typing import Optional, _GenericAlias, Callable
from pydantic import BaseModel
import fastflows
from fastflows import errors
from fastflows.schemas.misc import DefaultAPIResponseModel


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
                    raise fastflows.errors.FastFlowException(
                        f"Error API response: {response.text}. Status code: {response.status_code}"
                    )
            except Exception as e:

                logging.error(e)

                err_msg = (
                    message.format(args[1:] if len(args) > 1 else kwargs)
                    if args_in_message
                    else message
                )
                if append_api_error:
                    err_msg += f" {e.args[0]}"
                raise errors.FastFlowException(err_msg)

        return wrapper

    return decorator
