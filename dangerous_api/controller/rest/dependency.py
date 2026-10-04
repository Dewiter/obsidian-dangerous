from typing import Annotated

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException

from dangerous_api.bootstrap.container import commodity_service
from dangerous_api.configs.setting import settings
from dangerous_api.domain.user import User
from dangerous_api.pkg.security import Argon2Hasher, decode_access_token
from dangerous_api.service.commodity import CommodityService
from dangerous_api.service.user import UserService
from dangerous_api.storage.postgres.session import get_session
from dangerous_api.storage.postgres.user import SqlUserRepository

SessionDep = Annotated[AsyncSession, Depends(get_session)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
_hasher = Argon2Hasher()


def get_user_service(session: SessionDep) -> UserService:
    return UserService(SqlUserRepository(session), _hasher)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], svc: UserServiceDep
) -> User:
    user_id = decode_access_token(token, settings.jwt_secret)
    user = await svc.get(user_id) if user_id else None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Invalid or expired token",
            headers={"www-Authenticate": "Bearer"},
        )
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_commodity_service() -> CommodityService:
    return commodity_service()


CommodityServiceDep = Annotated[CommodityService, Depends(get_commodity_service)]
