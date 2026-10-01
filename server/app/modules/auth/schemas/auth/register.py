from typing import Annotated

from pydantic import EmailStr, StringConstraints, field_validator
from sqlmodel import SQLModel


class RegisterRequest(SQLModel):
    """Input payload for user registration."""

    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=70)]
    email: EmailStr
    password: str
    is_super_admin: bool = False

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if len(normalized) < 2:
            raise ValueError("El campo debe tener al menos 2 caracteres")
        return normalized
