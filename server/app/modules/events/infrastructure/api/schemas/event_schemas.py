"""
app/modules/events/infrastructure/api/schemas/event_schemas.py

Esquemas de validación y serialización de FastAPI para el módulo de eventos.
"""

from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel


class EventListItemRead(SQLModel):
    """Representación pública resumida de un evento para tarjetas y listados."""

    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    creator_name: str | None = None


class EventListRead(SQLModel):
    """Respuesta con la lista de eventos activos."""

    items: list[EventListItemRead]
