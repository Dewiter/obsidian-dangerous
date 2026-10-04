import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from dangerous_api.configs.setting import settings
from dangerous_api.controller.rest.dependency import CurrentUserDep, UserServiceDep
from dangerous_api.domain.errors import InvalidCredentials, UserAlreadyExists
from dangerous_api.domain.user import User
from dangerous_api.pkg.security import create_access_token

router = APIRouter(tags=["user"])


class RegisterIn(BaseModel):
    login: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserOut(BaseModel):
    id: uuid.UUID
    login: str
    email: EmailStr
    frontier_linked: bool

    @classmethod
    def from_domain(cls, user: User) -> UserOut:
        return cls(
            id=user.id,
            login=user.login,
            email=user.email,
            frontier_linked=user.frontier is not None,
        )


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterIn, svc: UserServiceDep):
    try:
        user = await svc.register(body.login, body.email, body.password)
    except UserAlreadyExists:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "Login or email already in use"
        ) from None
    return UserOut.from_domain(user)


@router.post("/auth/login", response_model=TokenOut)
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], svc: UserServiceDep
):
    try:
        user = await svc.authenticate(form.username, form.password)
    except InvalidCredentials:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Wrong login or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
    token = create_access_token(user.id, settings.jwt_secret, settings.jwt_duration)
    return TokenOut(access_token=token)


@router.get("/users/me", response_model=UserOut)
async def me(current: CurrentUserDep):
    return UserOut.from_domain(current)
