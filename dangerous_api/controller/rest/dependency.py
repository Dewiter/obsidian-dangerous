from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from dangerous_api.bootstrap.container import commodity_service
from dangerous_api.configs.setting import settings
from dangerous_api.domain.user import User
from dangerous_api.pkg.security import Argon2Hasher, decode_access_token
from dangerous_api.service.commodity import CommodityService
from dangerous_api.service.user.authenticate import AuthenticateUser
from dangerous_api.service.user.get_user import GetUser
from dangerous_api.service.user.link_frontier import LinkFrontier
from dangerous_api.service.user.register import RegisterUser
from dangerous_api.storage.postgres.session import get_session
from dangerous_api.storage.postgres.user.repository import SqlUserRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
_hasher = Argon2Hasher()


def get_register_user(session: SessionDep) -> RegisterUser:
    return RegisterUser(SqlUserRepository(session), _hasher)


def get_authenticate_user(session: SessionDep) -> AuthenticateUser:
    return AuthenticateUser(SqlUserRepository(session), _hasher)


def get_get_user(session: SessionDep) -> GetUser:
    return GetUser(SqlUserRepository(session))


def get_link_frontier(session: SessionDep) -> LinkFrontier:
    return LinkFrontier(SqlUserRepository(session))


RegisterUserDep = Annotated[RegisterUser, Depends(get_register_user)]
AuthenticateUserDep = Annotated[AuthenticateUser, Depends(get_authenticate_user)]
GetUserDep = Annotated[GetUser, Depends(get_get_user)]
LinkFrontierDep = Annotated[LinkFrontier, Depends(get_link_frontier)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], get_user: GetUserDep
) -> User:
    user_id = decode_access_token(token, settings.jwt_secret)
    user = await get_user(user_id) if user_id else None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_commodity_service() -> CommodityService:
    return commodity_service()


CommodityServiceDep = Annotated[CommodityService, Depends(get_commodity_service)]
