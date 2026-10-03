"""
app/modules/events/infrastructure/persistence/mappers/event_mapper.py

Traductor puro bidireccional entre la entidad Event y el modelo EventModel.
"""

from app.modules.events.domain.entities.event import Event
from app.modules.events.infrastructure.persistence.models.event_model import EventModel


class EventMapper:
    """Mapeo entre entidad de dominio Event y modelo de persistencia EventModel."""

    @staticmethod
    def to_domain(model: EventModel) -> Event:
        return Event(
            id=model.id,
            name=model.name,
            owner_id=model.owner_id,
            image_url=model.image_url,
            date=model.date,
            is_active=model.deleted_date is None,
        )

    @staticmethod
    def to_model(entity: Event) -> EventModel:
        return EventModel(
            id=entity.id,
            name=entity.name,
            owner_id=entity.owner_id,
            image_url=entity.image_url,
            date=entity.date,
        )
