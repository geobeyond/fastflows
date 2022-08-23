"""Main module."""
from typing import Any
import logging
import loguru
import uvicorn
from time import sleep
from fastflows.config.app import configuration as cfg
from fastflows.config.auth import opa_config
from fastflows.config.logging import create_logger
from fastflows.utils.app_exceptions import app_exception_handler
from fastflows.utils.app_exceptions import AppExceptionError
from fastflows.utils.request_exceptions import http_exception_handler
from fastflows.utils.request_exceptions import request_validation_exception_handler
from fastflows.routers import flows, flow_runs
from fastflows.errors import FastFlowException

from fastflows.core.catalog import Catalog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi_opa import OPAMiddleware
from mangum import Mangum
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware
from fastflows.providers import provider


class FastFlowsAPI(FastAPI):
    """Subclass of FastAPI that possesses a logger attribute."""

    def __init__(self, **extra: Any):
        """Included the self.logger attribute."""
        super().__init__(**extra)
        self.logger: loguru.Logger = loguru.logger


def create_app() -> FastFlowsAPI:
    """Handle application creation."""
    app = FastFlowsAPI(title="FastFlowsApi", root_path=cfg.ROOT_PATH, debug=True)

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(StarletteHTTPException)
    async def custom_http_exception_handler(request, e):
        return await http_exception_handler(request, e)

    @app.exception_handler(RequestValidationError)
    async def custom_validation_exception_handler(request, e):
        return await request_validation_exception_handler(request, e)

    @app.exception_handler(AppExceptionError)
    async def custom_app_exception_handler(request, e):
        return await app_exception_handler(request, e)

    if cfg.OPA_URL:
        app.add_middleware(OPAMiddleware, config=opa_config)

    app.logger = create_logger(name="app.main")

    return app


app = create_app()


@app.on_event("startup")
async def startup_event():

    if cfg.FASTFLOWS_PROVIDER_PREPARE_AT_THE_START:
        provider.healthcheck()

    if cfg.FASTFLOWS_AUTO_DEPLOYMENT == 1:
        logging.info(f"Register Flows in {provider.type.capitalize()} provider")
        try:
            Catalog().register_and_deploy()
        except FastFlowException:
            # error during connection to DB, maybe problem at the prefect start
            # let's wait & try one more time
            sleep(10)
            Catalog().register_and_deploy()


app.include_router(flows.router)
app.include_router(flow_runs.router)


def app_run():
    uvicorn.run(
        "fastflows.main:app",
        host=cfg.FASTFLOWS_HOST,
        port=cfg.FASTFLOWS_PORT,
        reload=cfg.RELOAD,
        access_log=cfg.ACCESS_LOG,
    )


if cfg.AWS_LAMBDA_DEPLOY:
    # to make it work with Amazon Lambda,
    # we create a handler object
    handler = Mangum(app)

if __name__ == "__main__":
    app_run()
