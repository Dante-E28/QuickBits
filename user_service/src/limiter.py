from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from src.error_messages import ERROR_MESSAGE, TOO_MANY_REQUESTS

limiter = Limiter(key_func=get_remote_address, default_limits=['50/minute'])


def rate_limit_exceeded_handler(
    request: Request,
    exc: RateLimitExceeded
) -> Response:
    response = JSONResponse(
        {'detail': {ERROR_MESSAGE: TOO_MANY_REQUESTS}},
        status_code=status.HTTP_429_TOO_MANY_REQUESTS
    )
    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
    return response
