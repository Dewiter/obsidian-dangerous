import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from inara.domain.user import FrontierAccount, User
from inara.storage.postgres.models import FrontierAccountRow, UserRow


def _to_domain(row: UserRow) -> User:
    f = row.frontier
    return User(
        id=row.id,
        login=row.login,
        email=row.email,
        password_hash=row.password_hash,
        frontier=FrontierAccount(
            f.frontier_id, f.access_token, f.refresh_token, f.expires_at
        )
        if f
        else None,
    )


class SqlUserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        self.session.add(
            UserRow(
                id=user.id,
                login=user.login,
                email=user.email,
                password_hash=user.password_hash,
            )
        )
        await self.session.commit()

    async def get(self, user_id: str) -> User | None:
        row = await self.session.get(UserRow, user_id)
        return _to_domain(row) if row else None

    async def get_by_login(self, login: str) -> User | None:
        row = await self.session.scalar(select(UserRow).where(UserRow.login == login))
        return _to_domain(row) if row else None

    async def get_by_frontier_id(self, frontier_id: str) -> User | None:
        row = await self.session.scalar(
            select(UserRow)
            .join(FrontierAccountRow)
            .where(FrontierAccountRow.user_id == frontier_id)
        )
        return _to_domain(row) if row else None

    async def link_frontier(self, user_id: uuid.UUID, account: FrontierAccount) -> None:
        await self.session.merge(
            FrontierAccountRow(
                user_id=user_id,
                frontier_id=account.frontier_id,
                access_token=account.access_token,
                refresh_token=account.refresh_token,
                expires_at=account.expires_at,
            )
        )
        await self.session.commit()
