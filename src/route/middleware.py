import json
import logging
from dataclasses import dataclass
from traceback import format_exc, print_exception
from uuid import uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("route.middleware")


@dataclass
class ExceptionConfiguration:
    """
    Configuration class for handling exceptions in the application.

    Attributes:
        exception (type[Exception]): The type of exception to be handled.
        status_code (int): The HTTP status code to be returned when the exception is raised.
        app_code (str): The application-specific code associated with the exception.
    """
    exception: type[Exception]
    status_code: int
    app_code: str


class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling exceptions in an HTTP application.

    Args:
        app: The ASGI application.
        exception_map (list[ExceptionConfiguration]): A list of exception configurations to handle.
        store_traceback (bool): Flag to determine if traceback should be stored in log files. Defaults to False.

    Example:
        exception_map = [
            ExceptionConfiguration(exception=NotAuthorizedException, status_code=403, app_code="ACL_NOT_ALLOWED")
        ]
        app.add_middleware(ExceptionHandlingMiddleware, exception_map=exception_map)
    """
    def __init__(self, app, exception_map: list[ExceptionConfiguration], store_traceback: bool = False):
        super().__init__(app)
        self._exeption_map = exception_map
        self._store_traceback = store_traceback

    async def dispatch(self, request: Request, call_next):
        excs = tuple([e.exception for e in self._exeption_map])
        request_id = uuid4()
        try:
            response = await call_next(request)
            response.headers["X-Request-ID"] = str(request_id)
            return response
        except excs as e:
            logger.exception(e, extra=dict(request_id=request_id))
            # if not self._store_traceback:
            #     traceback_file = f"/logs/{request_id}.{e.__class__.__name__}.log"
            #     logger.debug(f"Traceback stored in {traceback_file}")
            #     with open (traceback_file, "w+") as f:
            #         f.write(f"{e!s}\n\n")
            #         f.write(format_exc())
            # for exc in self._exeption_map:
            #     if isinstance(e, exc.exception):
            #         return Response(
            #             status_code=exc.status_code,
            #             content=json.dumps(dict(
            #                 code=exc.app_code,
            #                 message=str(e),
            #                 request_id=str(request_id)
            #             )),
            #             headers={
            #                 "Content-type": "application/json",
            #                 "X-Request-ID": str(request_id)
            #             }
            #         )
        except Exception as e:
            logger.error(e, extra=dict(request_id=request_id))
            print_exception(e)
            # if not self._store_traceback:
            #     traceback_file = f"/logs/{request_id}.{e.__class__.__name__}.log"
            #     logger.debug(f"Traceback stored in {traceback_file}")
            #     with open (traceback_file, "w+") as f:
            #         f.write(f"{e!s}\n\n")
            #         f.write(format_exc())
            return Response(
                status_code=500,
                content=json.dumps(dict(
                    code="FUCK...",
                    message=str(e),
                    request_id=str(request_id)
                )),
                headers={
                    "Content-type": "application/json",
                    "X-Request-ID": str(request_id)
                }
            )
