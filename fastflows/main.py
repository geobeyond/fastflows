from time import sleep

import fastapi
import fastapi_opa
import fastapi_opa.auth as opa_auth
import mangum
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from . import middleware
from .config import settings
from .core import catalog
from .errors import FastFlowException
from .providers import provider
from .routers.flows import router as flows_router
from .routers.flow_runs import router as flow_runs_router
from .utils.app_exceptions import (
    AppExceptionError,
    app_exception_handler,
)
from .utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)

_middleware = [
    Middleware(middleware.FastFlowsRequestIdMiddleware),
    Middleware(middleware.FastFlowsLoggingMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

if settings.AUTH.OPA_URL:
    _middleware.append(
        Middleware(
            fastapi_opa.OPAMiddleware,
            config=fastapi_opa.OPAConfig(
                authentication=opa_auth.OIDCAuthentication(
                    opa_auth.OIDCConfig(
                        well_known_endpoint=settings.AUTH.OIDC_WELL_KNOWN_ENDPOINT,
                        app_uri=settings.UVICORN.HOST,  # host where this app is running
                        client_id=settings.AUTH.OIDC_CLIENT_ID,
                        client_secret=settings.AUTH.OIDC_CLIENT_SECRET,
                    )
                ),
                opa_host=settings.AUTH.OPA_URL,
            ),
        )
    )


async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


def check_provider_health_task():
    if settings.PROVIDER_PREPARE_AT_THE_START:
        logger.info("Checking if provider is healthy...")
        provider.healthcheck()


def register_flows_task():
    if settings.AUTO_DEPLOYMENT:
        logger.info(f"Register Flows in {provider.type.capitalize()} provider")
        try:
            catalog.Catalog().register_and_deploy()
        except FastFlowException:
            # error during connection to DB, maybe problem at the prefect start
            # let's wait & try one more time
            sleep(10)
            catalog.Catalog().register_and_deploy()


app = fastapi.FastAPI(
    title="FastFlows",
    root_path=settings.ROOT_PATH,
    debug=settings.DEBUG,
    middleware=_middleware,
    on_startup=[check_provider_health_task, register_flows_task],
    exception_handlers={
        StarletteHTTPException: custom_http_exception_handler,
        RequestValidationError: custom_validation_exception_handler,
        AppExceptionError: custom_app_exception_handler,
    },
)

app.include_router(flows_router)
app.include_router(flow_runs_router)


if settings.AWS_LAMBDA_DEPLOY:
    # to make it work with Amazon Lambda,
    # we create a handler object
    handler = mangum.Mangum(app)
