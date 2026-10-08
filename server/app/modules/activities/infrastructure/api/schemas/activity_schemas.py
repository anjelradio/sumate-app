from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import Form
from sqlmodel import Field, SQLModel

from app.modules.activities.domain.exceptions import InvalidActivityDateException


class CreateActivityRequest(SQLModel):
    """Petición para registrar una nueva actividad."""

    name: str = Field(description="Nombre de la actividad")
    date: datetime = Field(description="Fecha y hora de realización de la actividad")
    capacity: int = Field(default=1, description="Cantidad de cupos o plazas")

    @classmethod
    def as_form(
        cls,
        name: Annotated[str, Form(description="Nombre de la actividad")],
        date: Annotated[str, Form(description="Fecha y hora de realización de la actividad")],
        capacity: Annotated[int, Form(description="Cantidad de cupos o plazas")] = 1,
    ) -> "CreateActivityRequest":
        clean_date_str = date.strip().replace("Z", "+00:00")
        try:
            parsed_date = datetime.fromisoformat(clean_date_str)
            if parsed_date.tzinfo is None:
                parsed_date = parsed_date.replace(tzinfo=timezone.utc)
        except ValueError:
            raise InvalidActivityDateException("El formato de la fecha es inválido. Use ISO 8601 o YYYY-MM-DDTHH:MM.")

        return cls(
            name=name,
            date=parsed_date,
            capacity=capacity,
        )



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


class MyActivityListItemRead(SQLModel):
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    registered_count: int
    creator_name: str | None = None
    creator_image: str | None = None


class MyActivityListRead(SQLModel):
    items: list[MyActivityListItemRead]


class ActivityDetailDataRead(SQLModel):
    id: UUID
    activity_id: UUID
    latitude: float | None = None
    longitude: float | None = None
    place: str | None = None
    address: str | None = None
    description: str | None = None


class ActivityParticipantRead(SQLModel):
    id: str
    name: str
    image: str | None = None


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
    is_participating: bool = False
    participants: list[ActivityParticipantRead] = []
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


class UpdateActivityCapacityRequest(SQLModel):
    capacity: int

