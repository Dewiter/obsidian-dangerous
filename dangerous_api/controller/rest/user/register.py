from fastapi import APIRouter, HTTPException, status

from dangerous_api.controller.rest.dependency import RegisterUserDep
from dangerous_api.controller.rest.user.schemas import RegisterIn, UserOut
from dangerous_api.domain.errors import UserAlreadyExists

router = APIRouter()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterIn, register_user: RegisterUserDep):
    try:
        user = await register_user(body.login, body.email, body.password)
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Login or email already in use"
        ) from None
    return UserOut.from_domain(user)
