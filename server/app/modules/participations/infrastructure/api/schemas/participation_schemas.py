from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel


class ParticipatedActivityItemRead(SQLModel):
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    enrolled_date: datetime
    is_past: bool
    creator_name: str | None = None
    creator_image: str | None = None


class ParticipatedActivityListRead(SQLModel):
    items: list[ParticipatedActivityItemRead]
