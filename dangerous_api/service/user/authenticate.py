import asyncio

from dangerous_api.domain.errors import InvalidCredentials
from dangerous_api.domain.user import User
from dangerous_api.service.user.ports import PasswordHasher, UserRepository


class AuthenticateUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    async def __call__(self, login: str, password: str) -> User:
        user = await self.repo.get_by_login(login)
        if user is None:
            await asyncio.to_thread(
                self.hasher.verify, password, self.hasher.dummy_hash
            )
            raise InvalidCredentials
        if not await asyncio.to_thread(
            self.hasher.verify, password, user.password_hash
        ):
            raise InvalidCredentials
        return user
