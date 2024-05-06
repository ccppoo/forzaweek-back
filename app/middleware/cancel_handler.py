from starlette.responses import Response
from starlette.requests import Request
from starlette.status import HTTP_204_NO_CONTENT

__all__ = ["suppress_no_response"]


async def suppress_no_response(request: Request, call_next):
    try:
        return await call_next(request)
    except RuntimeError as exc:
        if str(exc) == "No response returned." and await request.is_disconnected():
            return Response(status_code=HTTP_204_NO_CONTENT)
