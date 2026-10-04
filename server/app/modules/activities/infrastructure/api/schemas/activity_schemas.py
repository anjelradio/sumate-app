from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel


class ActivityListItemRead(SQLModel):
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    creator_name: str | None = None
    creator_image: str | None = None


class ActivityListRead(SQLModel):
    items: list[ActivityListItemRead]


class ActivityDetailDataRead(SQLModel):
    id: UUID
    activity_id: UUID
    latitude: float | None = None
    longitude: float | None = None
    place: str | None = None
    address: str | None = None
    description: str | None = None


class ActivityDetailRead(SQLModel):
    id: UUID
    name: str
    owner_id: str
    creator_name: str | None = None
    creator_image: str | None = None
    image_url: str
    date: datetime
    capacity: int
    status: str
    is_owner: bool
    detail: ActivityDetailDataRead | None = None


class UpdateLocationRequest(SQLModel):
    latitude: float
    longitude: float
    place: str | None = None


class UpdateDescriptionRequest(SQLModel):
    description: str


class UpdateActivityInfoRequest(SQLModel):
    name: str | None = None
    date: datetime | None = None
    capacity: int | None = None

