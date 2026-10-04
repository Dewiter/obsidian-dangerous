from fastapi import APIRouter

from dangerous_api.controller.rest.user import login, me, register

router = APIRouter(tags=["user"])
router.include_router(register.router)
router.include_router(login.router)
router.include_router(me.router)
