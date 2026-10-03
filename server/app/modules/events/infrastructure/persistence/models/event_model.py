"""
app/modules/events/infrastructure/persistence/models/event_model.py

Modelo de persistencia SQLModel para eventos.
Hereda de BaseModel (soft-delete vía deleted_date, id UUIDv4, created_date, modified_date).
"""

from datetime import datetime
from sqlmodel import Field

from app.shared.infrastructure.db.base_model import BaseModel


class EventModel(BaseModel, table=True):
    __tablename__ = "events"

    name: str = Field(index=True, nullable=False)
    owner_id: str = Field(index=True, nullable=False)
    image_url: str = Field(nullable=False)
    date: datetime = Field(index=True, nullable=False)
