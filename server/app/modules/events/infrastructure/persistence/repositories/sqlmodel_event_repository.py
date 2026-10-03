"""
app/modules/events/infrastructure/persistence/repositories/sqlmodel_event_repository.py

Implementación de EventRepository utilizando SQLModel / SQLAlchemy Session.
Cumple con convenciones de nomenclatura, filtrado de deleted_date y métodos de persistencia.
"""

from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session, select

from app.modules.events.domain.entities.event import Event
from app.modules.events.domain.repositories.event_repository import EventRepository
from app.modules.events.infrastructure.persistence.mappers.event_mapper import EventMapper
from app.modules.events.infrastructure.persistence.models.event_model import EventModel


class SQLModelEventRepository(EventRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, event_id: UUID) -> Event | None:
        statement = select(EventModel).where(
            EventModel.id == event_id,
            EventModel.deleted_date.is_(None),
        )
        record = self.db.exec(statement).first()
        return EventMapper.to_domain(record) if record else None

    def list_events(
        self,
        *,
        owner_id: str | None = None,
        exclude_owner_id: str | None = None,
    ) -> list[Event]:
        statement = select(EventModel).where(EventModel.deleted_date.is_(None))

        if owner_id:
            statement = statement.where(EventModel.owner_id == owner_id)
        elif exclude_owner_id:
            statement = statement.where(EventModel.owner_id != exclude_owner_id)

        # Ordenar por fecha de realización más próxima primero
        statement = statement.order_by(EventModel.date.asc())
        records = self.db.exec(statement).all()
        return [EventMapper.to_domain(record) for record in records]

    def save(self, event: Event) -> None:
        record = self.db.get(EventModel, event.id)
        if record is None:
            model = EventMapper.to_model(event)
            if not event.is_active:
                model.deleted_date = datetime.now(timezone.utc)
            self.db.add(model)
            return

        record.name = event.name
        record.owner_id = event.owner_id
        record.image_url = event.image_url
        record.date = event.date

        if event.is_active:
            record.deleted_date = None
        elif record.deleted_date is None:
            record.deleted_date = datetime.now(timezone.utc)

        record.modified_date = datetime.now(timezone.utc)
