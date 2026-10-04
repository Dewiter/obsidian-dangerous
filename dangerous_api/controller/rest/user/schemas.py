import uuid

from pydantic import BaseModel, EmailStr, Field

from dangerous_api.domain.user import User


class RegisterIn(BaseModel):
    login: str = Field(min_length=3, max_length=64, pattern=r"^[A-Za-z0-9_.-]+$")
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)


class UserOut(BaseModel):
    id: uuid.UUID
    login: str
    email: EmailStr
    frontier_linked: bool

    @classmethod
    def from_domain(cls, user: User) -> UserOut:
        return cls(
            id=user.id,
            login=user.login,
            email=user.email,
            frontier_linked=user.frontier is not None,
        )


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
