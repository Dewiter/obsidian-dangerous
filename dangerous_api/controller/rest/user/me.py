from fastapi import APIRouter

from dangerous_api.controller.rest.dependency import CurrentUserDep
from dangerous_api.controller.rest.user.schemas import UserOut

router = APIRouter()


@router.get("/users/me", response_model=UserOut)
async def me(current: CurrentUserDep):
    return UserOut.from_domain(current)
