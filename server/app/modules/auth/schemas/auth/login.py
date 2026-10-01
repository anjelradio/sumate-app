from pydantic import EmailStr
from sqlmodel import SQLModel

from app.modules.auth.schemas.common import UserRead


class LoginRequest(SQLModel):
    """Input payload for email/password login."""

    email: EmailStr
    password: str


class LoginResponse(SQLModel):
    """Auth response payload with user data and access token."""

    user: UserRead
    access_token: str
