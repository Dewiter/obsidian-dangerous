from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from dangerous_api.controller.rest.dependency import AuthenticateUserDep
from dangerous_api.controller.rest.user.schemas import UserOut
from dangerous_api.domain.errors import UserAlreadyExists

router = APIRouter()


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    authenticate: AuthenticateUserDep,
):
    try:
        user = await authenticate(form.username, form.password)
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Login or email already in use"
        ) from None
    return UserOut.from_domain(user)
