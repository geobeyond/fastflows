import logging
from time import sleep

import fastapi
import fastapi_opa
import fastapi_opa.auth as opa_auth
import mangum
from fastapi.exceptions import RequestValidationError
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.cors import CORSMiddleware

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


app = fastapi.FastAPI(
    title="FastFlows",
    root_path=settings.ROOT_PATH,
    debug=settings.DEBUG,
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.AUTH.OPA_URL:
    app.add_middleware(
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

app.include_router(flows_router)
app.include_router(flow_runs_router)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)


@app.exception_handler(AppExceptionError)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)


@app.on_event("startup")
async def startup_event():
    logger.info("Hello!")

    if settings.PROVIDER_PREPARE_AT_THE_START:
        provider.healthcheck()

    if settings.AUTO_DEPLOYMENT:
        logging.info(f"Register Flows in {provider.type.capitalize()} provider")
        try:
            catalog.Catalog().register_and_deploy()
        except FastFlowException:
            # error during connection to DB, maybe problem at the prefect start
            # let's wait & try one more time
            sleep(10)
            catalog.Catalog().register_and_deploy()


if settings.AWS_LAMBDA_DEPLOY:
    # to make it work with Amazon Lambda,
    # we create a handler object
    handler = mangum.Mangum(app)
