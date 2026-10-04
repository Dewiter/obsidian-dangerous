from dangerous_api.domain.user import FrontierAccount, User
from dangerous_api.storage.postgres.models import UserRow


def to_domain(row: UserRow) -> User:
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
