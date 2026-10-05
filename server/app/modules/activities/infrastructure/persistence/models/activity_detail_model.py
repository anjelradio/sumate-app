from uuid import UUID

from app.shared.infrastructure.db.base_model import BaseModel
from sqlmodel import Field


class ActivityDetailModel(BaseModel, table=True):
    __tablename__ = "activity_detail"

    activity_id: UUID = Field(foreign_key="activity.id", unique=True, index=True, nullable=False)
    latitude: float | None = Field(default=None, nullable=True)
    longitude: float | None = Field(default=None, nullable=True)
    place: str | None = Field(default=None, max_length=255, nullable=True)
    address: str | None = Field(default=None, max_length=500, nullable=True)
    description: str | None = Field(default=None, nullable=True)
