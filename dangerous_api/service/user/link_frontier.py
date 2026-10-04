import uuid

from dangerous_api.domain.user import FrontierAccount
from dangerous_api.service.user.ports import UserRepository


class LinkFrontier:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def __call__(self, user_id: uuid.UUID, account: FrontierAccount) -> None:
        await self.repo.link_frontier(user_id, account)
