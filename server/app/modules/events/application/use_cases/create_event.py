"""
app/modules/events/application/use_cases/create_event.py

Caso de uso: Crear un nuevo evento convocante.
Orquesta la validación del dominio, la persistencia en el repositorio y la confirmación transaccional (UoW).
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repositories.event_repository import EventRepository
from app.shared.application.ports import UnitOfWork


@dataclass(slots=True)
class CreateEventCommand:
    name: str
    owner_id: str
    image_url: str
    date: datetime


class CreateEventUseCase:
    def __init__(self, event_repository: EventRepository, uow: UnitOfWork) -> None:
        self.event_repository = event_repository
        self.uow = uow

    def execute(self, command: CreateEventCommand) -> UUID:
        event = Event.create(
            name=command.name,
            owner_id=command.owner_id,
            image_url=command.image_url,
            date=command.date,
        )
        self.event_repository.save(event)
        self.uow.commit()
        return event.id
