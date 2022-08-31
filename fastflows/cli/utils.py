import typer
import sys
import json
from ast import literal_eval
from typing import Optional
from functools import wraps
import traceback
from fastflows.config.app import configuration as cfg


def process_parmas_input_as_a_comma_separated_string(params: str) -> dict:
    # mean format like --params a=1
    parameters = {}
    params = params.split(",")
    for pair in params:
        key, value = pair.split("=", 1)
        parameters[key] = value
    return parameters


def process_parmas_as_a_string_with_dict(params) -> dict:
    try:
        # if it was n't json - try eval
        return json.loads(params)
    except ValueError:
        pass
    try:
        return literal_eval(params)
    except ValueError:
        raise ValueError(
            f'Invalid format of parameters. Possible you forget quotes near names. Should be like in example: \'{{"a": "b"}}\'. You pass: {params}'
        )


def process_params_from_str(params: Optional[str]) -> dict:
    # because it is for Typer call back - it will be called always,
    # but value must be processed only if provided by user
    if params is None:
        return {}
    params = params.strip()
    if "=" in params:
        parameters: dict = process_parmas_input_as_a_comma_separated_string(params)
    elif params.startswith("{") and params.endswith("}"):
        # mean expected --params {"a": "b"}
        parameters: dict = process_parmas_as_a_string_with_dict(params)
    else:
        raise ValueError(
            f"Invalid format of parameters. Should be like 'a=1,b=2' or '{{\"a\": \"b\"}}'. You pass: {params}"
        )
    return parameters


def catch_exceptions(func):
    """decorator to remove traceback in command line & convert output to red beutiful error message,
    to disable option & see traceback: set env FASTFLOW_DEBUG = 1
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            if cfg.FASTFLOW_DEBUG == 1:
                typer.echo(traceback.format_exc())
            message = f"\n{e.args[0]}"
            typer.secho(message, fg=typer.colors.RED, err=True)
            sys.exit(1)

    return wrapper
