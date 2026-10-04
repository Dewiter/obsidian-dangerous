import asyncio
import uuid
from typing import Protocol

from dangerous_api.domain.errors import InvalidCredentials, UserAlreadyExists
from dangerous_api.domain.user import FrontierAccount, User


class UserRepository(Protocol):
    async def add(self, user: User) -> None: ...
    async def get(self, user_id: uuid.UUID) -> User | None: ...
    async def get_by_login(self, login: str) -> User | None: ...
    async def get_by_email(self, email: str) -> User | None: ...
    async def get_by_frontier_id(self, frontier_id: int) -> User | None: ...
    async def link_frontier(
        self, user_id: uuid.UUID, account: FrontierAccount
    ) -> None: ...


class PasswordHasher(Protocol):
    dummy_hash: str

    def hash(self, password: str) -> str: ...
    def verify(self, password: str, hashed: str) -> bool: ...


class UserService:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    async def register(self, login: str, email: str, password: str) -> User:
        email = email.lower()
        if await self.repo.get_by_login(login) or await self.repo.get_by_email(email):
            raise UserAlreadyExists
        password_hash = await asyncio.to_thread(self.hasher.hash, password)
        user = User(
            id=uuid.uuid4(),
            login=login,
            email=email,
            password_hash=password_hash,
        )
        await self.repo.add(user)
        return user

    async def authenticate(self, login: str, password: str) -> User:
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

    async def get(self, user_id: uuid.UUID) -> User | None:
        return await self.repo.get(user_id)

    async def link_frontier(self, user_id: uuid.UUID, account: FrontierAccount) -> None:
        await self.repo.link_frontier(user_id, account)
