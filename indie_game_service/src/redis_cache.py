import hashlib
from typing import Callable, Optional

from fastapi_cache import FastAPICache
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


def no_uow_key_builder(
    func: Callable,
    namespace: Optional[str] = "",
    request: Optional[Request] = None,
    response: Optional[Response] = None,
    args: Optional[tuple] = None,
    kwargs: Optional[dict] = None,
) -> str:
    """Key builder without uow dependency."""
    from fastapi_cache import FastAPICache

    prefix = f"{FastAPICache.get_prefix()}:{namespace}:"
    if kwargs:
        no_uow_kw = kwargs.copy()
        if kwargs.get('uow'):
            no_uow_kw.pop('uow')
    cache_key = (
        prefix
        + hashlib.md5(  # nosec:B303
            f"{func.__module__}:{func.__name__}:{args}:{no_uow_kw}".encode()
        ).hexdigest()
    )
    return cache_key


async def clear_cache(func, namespace: str, kwargs: dict | None = None):
    """Clear cache by key in redis."""
    key_builder = FastAPICache.get_key_builder()
    cache_key = key_builder(
        func=func,
        namespace=namespace,
        args=(),
        kwargs=kwargs
    )
    await FastAPICache.get_backend().clear(key=cache_key)


disable_cache_routes = [
    '/comments'
]


class RouterCacheControlResetMiddleware(BaseHTTPMiddleware):
    """Disable Response headers Cache-Control (set to 'no-cache').

    The initial reason for this is that the fastapi-cache library sets
    the max-age param of the header equal to the expire parameter
    that is provided to the caching layer (Redis), so the response is
     also cached on the browser side, which in most cases is unnecessary."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> Response:
        response: Response = await call_next(request)
        if (
            request.url.path in disable_cache_routes
            and request.method == 'GET'
        ):
            response.headers.update({
                "Cache-Control": "no-cache"
            })
        return response
