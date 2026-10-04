from fastapi import APIRouter

from dangerous_api.controller.rest import user

api_router = APIRouter()
api_router.include_router(user.router)
