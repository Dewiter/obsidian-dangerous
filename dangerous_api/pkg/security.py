import uuid
from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

_hasher = PasswordHash.recommended()


class Argon2Hasher:
    dummy_hash = _hasher.hash("not-a-real-password")

    def hash(self, password: str) -> str:
        return _hasher.hash(password)

    def verify(self, password: str, hashed: str) -> bool:
        return _hasher.verify(password, hashed)


def create_access_token(user_id: uuid.UUID, secret: str, expires_minutes: int) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_access_token(token: str, secret: str) -> uuid.UUID | None:
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return uuid.UUID(payload["sub"])
    except jwt.InvalidTokenError, KeyError, ValueError:
        return None
