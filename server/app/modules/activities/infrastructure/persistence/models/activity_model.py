"""
app/modules/activities/infrastructure/persistence/models/activity_model.py

Modelo de persistencia SQLModel para actividades.
Hereda de BaseModel (soft-delete vía deleted_date, id UUIDv4, created_date, modified_date).
"""

from datetime import datetime
from sqlmodel import Field

from app.shared.infrastructure.db.base_model import BaseModel


class ActivityModel(BaseModel, table=True):
    __tablename__ = "activity"

    name: str = Field(index=True, nullable=False)
    owner_id: str = Field(index=True, nullable=False)
    image_url: str = Field(nullable=False)
    date: datetime = Field(index=True, nullable=False)
