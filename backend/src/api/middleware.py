from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        await self.authorize_request(request)

        response = await call_next(request)
        return response

    async def authorize_request(self, request: Request):
        # TODO: Add authorization
        pass