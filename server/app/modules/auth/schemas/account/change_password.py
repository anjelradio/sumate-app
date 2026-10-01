from typing import Annotated

from pydantic import StringConstraints, field_validator
from sqlmodel import SQLModel


class ChangePasswordRequest(SQLModel):
    """Input payload to change password for authenticated user."""

    current_password: Annotated[str, StringConstraints(min_length=1)]
    new_password: Annotated[str, StringConstraints(min_length=1)]
    confirm_new_password: Annotated[str, StringConstraints(min_length=1)]

    @field_validator("current_password", "new_password", "confirm_new_password")
    @classmethod
    def validate_password_required(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("La contrasena es requerida")
        return value
