"""custom middleware classes for fastflows."""

import typing
import uuid

import loguru
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware


class FastFlowsRequestIdMiddleware(BaseHTTPMiddleware):
    """Adds a request id to the current state.

    The request id, sometimes also known as correlation id, can be provided by
    the client, by means of setting the X-REQUEST-ID HTTP header. Alternatively, if
    not provided, this middleware generates a request id.

    This middleware is inspired by:

    - https://github.com/bigbag/starlette-request-id
    - https://github.com/snok/asgi-correlation-id

    """

    REQUEST_ID_HEADER: str

    def __init__(self, app, request_id_header: typing.Optional[str] = "x-request-id"):
        super().__init__(app)
        self.REQUEST_ID_HEADER = request_id_header

    async def dispatch(self, request: Request, call_next: typing.Callable) -> Response:
        request_id = request.headers.get(self.REQUEST_ID_HEADER, uuid.uuid4().hex)
        request.app.state.REQUEST_ID = request_id
        response: Response = await call_next(request)
        response.headers[self.REQUEST_ID_HEADER] = request_id
        return response


class FastFlowsLoggingMiddleware(BaseHTTPMiddleware):
    """Adds a contextualized logger to each request.

    The context set by this middleware on the logger is:

    - request_id: This is set to the current request id, as set by the
      `FastFlowsRequestIdMiddlewae` (which should have already processed the request
      before)

    The prepared logger is then stored in the app state object. It can be used inside
    a path operation function like this:

        `request.app.state.LOGGER.info("Hi world!")`

    """

    async def dispatch(self, request: Request, call_next: typing.Callable) -> Response:
        id_ = getattr(request.app.state, "REQUEST_ID", None)
        bound_logger = loguru.logger.bind(request_id=id_)
        request.app.state.LOGGER = bound_logger
        response = await call_next(request)
        return response
