"""
app/modules/activities/domain/repositories/activity_repository.py

Contrato abstracto del repositorio de actividades (Domain Repository).
Sin prefijo 'I' según directivas constitucionales.
"""

from abc import ABC, abstractmethod
from uuid import UUID

from app.modules.activities.domain.entities.activity import Activity


class ActivityRepository(ABC):
    """Contrato para persistencia y consulta de entidades Activity."""

    @abstractmethod
    def save(self, activity: Activity) -> None:
        """Persiste o actualiza una actividad en el almacenamiento."""
        ...

    @abstractmethod
    def get_by_id(self, activity_id: UUID) -> Activity | None:
        """Obtiene una actividad activa por su identificador UUID."""
        ...

    @abstractmethod
    def list_activities(
        self,
        *,
        owner_id: str | None = None,
        exclude_owner_id: str | None = None,
    ) -> list[Activity]:
        """
        Lista actividades activas ordenadas cronológicamente por su fecha de realización.

        - Si se provee owner_id: retorna únicamente actividades del usuario creador.
        - Si se provee exclude_owner_id: retorna únicamente actividades que NO pertenezcan al usuario creador.
        """
        ...
