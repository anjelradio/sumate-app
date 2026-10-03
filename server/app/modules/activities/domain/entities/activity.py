from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from app.modules.activities.domain.exceptions import (
    InvalidActivityDateException,
    InvalidActivityImageException,
    InvalidActivityNameException,
)


class ActivityStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    CLOSED = "closed"


class Activity:
    """Entidad central de una actividad o iniciativa comunitaria."""

    def __init__(
        self,
        id: UUID,
        name: str,
        owner_id: str,
        image_url: str,
        date: datetime,
        capacity: int = 1,
        status: ActivityStatus | str = ActivityStatus.DRAFT,
        creator_name: str | None = None,
    ) -> None:
        self.id = id
        self.name = self.normalize_name(name)
        self.owner_id = self.validate_owner_id(owner_id)
        self.image_url = self.validate_image_url(image_url)
        self.date = self.validate_date(date)
        self.capacity = self.validate_capacity(capacity)
        self.status = ActivityStatus(status) if isinstance(status, str) else status
        self.creator_name = creator_name

    @classmethod
    def create(
        cls,
        *,
        name: str,
        owner_id: str,
        image_url: str,
        date: datetime,
        capacity: int = 1,
        status: ActivityStatus | str = ActivityStatus.DRAFT,
        creator_name: str | None = None,
    ) -> Activity:
        """Fábrica de negocio: genera UUID y estado inicial en borrador."""
        return cls(
            id=uuid4(),
            name=name,
            owner_id=owner_id,
            image_url=image_url,
            date=date,
            capacity=capacity,
            status=status,
            creator_name=creator_name,
        )

    @staticmethod
    def normalize_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise InvalidActivityNameException("El nombre de la actividad no puede estar vacío.")
        return name.strip()

    @staticmethod
    def validate_owner_id(owner_id: str) -> str:
        if not isinstance(owner_id, str) or not owner_id.strip():
            raise ValueError("El identificador del creador (owner_id) es obligatorio.")
        return owner_id.strip()

    @staticmethod
    def validate_image_url(image_url: str) -> str:
        if not isinstance(image_url, str) or not image_url.strip():
            raise InvalidActivityImageException("La URL de la imagen de la actividad es requerida.")
        return image_url.strip()

    @staticmethod
    def validate_date(date: datetime) -> datetime:
        if not isinstance(date, datetime):
            raise InvalidActivityDateException("La fecha de la actividad debe ser un objeto datetime válido.")
        return date

    @staticmethod
    def validate_capacity(capacity: int) -> int:
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
            raise ValueError("La cantidad de plazas debe ser un número entero mayor a cero.")
        if capacity > 10000:
            raise ValueError("La cantidad de plazas no puede superar 10,000.")
        return capacity
