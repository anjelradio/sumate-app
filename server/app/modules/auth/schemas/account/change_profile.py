from typing import Annotated

from pydantic import StringConstraints, field_validator
from sqlmodel import SQLModel


class UpdateProfileRequest(SQLModel):
    """Input payload to update the current user profile."""

    first_name: Annotated[str, StringConstraints(min_length=2, max_length=50)]
    last_name: Annotated[str, StringConstraints(min_length=2, max_length=70)]

    @field_validator("first_name", "last_name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if len(normalized) < 2:
            raise ValueError("El campo debe tener al menos 2 caracteres")
        return normalized
