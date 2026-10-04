import asyncio
import uuid

from dangerous_api.domain.errors import UserAlreadyExists
from dangerous_api.domain.user import User
from dangerous_api.service.user.ports import PasswordHasher, UserRepository


class RegisterUser:
    def __init__(self, repo: UserRepository, hasher: PasswordHasher):
        self.repo = repo
        self.hasher = hasher

    async def __call__(self, login: str, email: str, password: str) -> User:
        email = email.lower()
        if await self.repo.get_by_login(login) or await self.repo.get_by_email(email):
            raise UserAlreadyExists
        password_hash = await asyncio.to_thread(self.hasher.hash, password)
        user = User(
            id=uuid.uuid4(), login=login, email=email, password_hash=password_hash
        )
        await self.repo.add(user)
        return user
