"""
app/modules/events/application/queries/list_events.py

Consulta para listar eventos según ámbito (propios del usuario o de otros miembros).
Devuelve DTOs inmutables de Python puro.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from app.modules.events.domain.repositories.event_repository import EventRepository


@dataclass(frozen=True, slots=True)
class ListEventsQuery:
    scope: Literal["mine", "others"]
    current_user_id: str


@dataclass(frozen=True, slots=True)
class EventListItemDTO:
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    creator_name: str | None = None


@dataclass(frozen=True, slots=True)
class EventListDTO:
    items: tuple[EventListItemDTO, ...]


class ListEventsQueryHandler:
    def __init__(self, event_repository: EventRepository) -> None:
        self.event_repository = event_repository

    def execute(self, query: ListEventsQuery) -> EventListDTO:
        if query.scope == "mine":
            events = self.event_repository.list_events(owner_id=query.current_user_id)
        else:
            events = self.event_repository.list_events(exclude_owner_id=query.current_user_id)

        items = tuple(
            EventListItemDTO(
                id=event.id,
                name=event.name,
                image_url=event.image_url,
                date=event.date,
                owner_id=event.owner_id,
                creator_name=None,
            )
            for event in events
        )

        return EventListDTO(items=items)
