from collections.abc import Callable
from datetime import datetime
import json
from typing import Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.concurrency import iterate_in_threadpool
from loguru import logger

class LoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Any]
    ) -> Response:
        """
        Logs all incoming and outgoing request, response pairs. This method logs the request params,
        datetime of request, duration of execution. Logs should be printed using the custom logging module provided.
        Logs should be printed so that they are easily readable and understandable.

        :param request: Request received to this middleware from client (it is supplied by FastAPI)
        :param call_next: Endpoint or next middleware to be called (if any, this is the next middleware in the chain of middlewares, it is supplied by FastAPI)
        :return: Response from endpoint
        """
        # TODO:(Member) Finish implementing this method
        start_time = datetime.now()
        response = await call_next(request)
        duration = (datetime.now() - start_time).total_seconds()
        date_t = start_time.strftime("%d/%m/%Y %H:%M")
        response_headers = dict(response.headers)
        # body = b""
        # async for chunk in response.body_iterator:
        #     body += chunk
        # response_body = body.decode("utf-8")
        response_body_chunks = [chunk async for chunk in response.body_iterator]
        response_body_str = b"".join(response_body_chunks).decode("utf-8")
        response_body_json = json.loads(response_body_str)
        response.body_iterator = iterate_in_threadpool(iter(response_body_chunks))
        logger.info(
            f"Request: {request.method} {request.url}; Response Code: {response.status_code}; Response Headers: {response_headers}; Response Body: {response_body_json}; DateTime called: {date_t}; Execution Duration: {duration:.6f}s"
        )
        return response
