import uuid

from dangerous_api.domain.user import User
from dangerous_api.service.user.ports import UserRepository


class GetUser:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def __call__(self, user_id: uuid.UUID) -> User | None:
        return await self.repo.get(user_id)
