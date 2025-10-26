from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from time import time

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.request_id = f"req_{int(time()*1000)}"
        response = await call_next(request)
        response.headers['X-Request-ID'] = request.state.request_id
        return response
