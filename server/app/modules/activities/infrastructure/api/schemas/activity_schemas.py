"""
app/modules/activities/infrastructure/api/schemas/activity_schemas.py

Esquemas de validación y serialización de FastAPI para el módulo de actividades.
"""

from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel


class ActivityListItemRead(SQLModel):
    """Representación pública resumida de una actividad para tarjetas y listados."""

    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    creator_name: str | None = None


class ActivityListRead(SQLModel):
    """Respuesta con la lista de actividades activas."""

    items: list[ActivityListItemRead]
