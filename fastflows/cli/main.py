import logging
import sys

import typer
import uvicorn
from loguru import logger
from uvicorn.config import LOGGING_CONFIG as UVICORN_LOGGING_CONFIG

from ..config import settings
from .flows import flows_app
from .flow_runs import flow_runs
from .task_runs import task_runs
from .utils import catch_exceptions

_common_log_handler_kwargs = {
    "level": settings.LOGGING.LEVEL.upper(),
    "diagnose": settings.LOGGING.LEVEL.upper() == "DEBUG",
    "colorize": None,  # loguru automatically chooses whether to colorize or not
    "backtrace": True,
    "enqueue": settings.LOGGING.ENQUEUE,
    "format": settings.LOGGING.FORMAT,
}

logger.configure(
    handlers=[
        {"sink": sys.stderr, **_common_log_handler_kwargs},
        {
            "sink": settings.LOGGING.PATH / settings.LOGGING.FILENAME,
            "retention": settings.LOGGING.RETENTION,
            "rotation": settings.LOGGING.ROTATION,
            **_common_log_handler_kwargs,
        },
    ]
)

app = typer.Typer()


@app.command()
@catch_exceptions
def server():
    """Start FastFlows server"""
    typer.echo("Starting FastFlows server")
    logger.info("Welcome")
    logging_config = UVICORN_LOGGING_CONFIG.copy()
    logging_config["handlers"]["fastflows"] = {
        "class": "fastflows.logging.LoguruInterceptHandler",
    }
    logging_config["loggers"] = {
        "uvicorn": {"handlers": ["fastflows"], "level": "INFO", "propagate": False},
        "uvicorn.error": {
            "handlers": ["fastflows"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["fastflows"],
            "level": "INFO",
            "propagate": False,
        },
    }
    uvicorn.run(
        "fastflows.main:app",
        host=settings.UVICORN.HOST,
        port=settings.UVICORN.PORT,
        reload=settings.UVICORN.RELOAD,
        access_log=settings.UVICORN.ACCESS_LOG,
        log_level=logging.getLevelName(settings.LOGGING.LEVEL),
        log_config=logging_config,
    )


app.add_typer(
    flows_app, name="flows", help="Operate with Flows: get state, update state"
)
app.add_typer(
    flow_runs, name="flow-runs", help="Operate with Flow Runs: get state, update state"
)

app.add_typer(
    task_runs, name="task-runs", help="Operate with Tasks Runs: get state, update state"
)
