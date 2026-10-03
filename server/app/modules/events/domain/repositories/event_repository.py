"""
app/modules/events/domain/repositories/event_repository.py

Contrato abstracto del repositorio de eventos (Domain Repository).
Sin prefijo 'I' según directivas constitucionales.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.events.domain.entities.event import Event


class EventRepository(ABC):
    """Contrato para persistencia y consulta de entidades Event."""

    @abstractmethod
    def save(self, event: Event) -> None:
        """Persiste o actualiza un evento en el almacenamiento."""
        ...

    @abstractmethod
    def get_by_id(self, event_id: UUID) -> Event | None:
        """Obtiene un evento activo por su identificador UUID."""
        ...

    @abstractmethod
    def list_events(
        self,
        *,
        owner_id: str | None = None,
        exclude_owner_id: str | None = None,
    ) -> list[Event]:
        """
        Lista eventos activos ordenados cronológicamente por su fecha de realización.

        - Si se provee owner_id: retorna únicamente eventos del usuario creador.
        - Si se provee exclude_owner_id: retorna únicamente eventos que NO pertenezcan al usuario creador.
        """
        ...
