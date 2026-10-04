from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from app.modules.activities.domain.entities.activity import Activity
from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.shared.application.ports import UnitOfWork
from app.shared.domain.exceptions import ForbiddenException, ValidationException


@dataclass(slots=True)
class PublishActivityCommand:
    activity_id: UUID
    owner_id: str


class PublishActivityUseCase:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        uow: UnitOfWork,
    ) -> None:
        self.activity_repository = activity_repository
        self.uow = uow

    def execute(self, command: PublishActivityCommand) -> Activity:
        result = self.activity_repository.get_detail_by_activity_id(command.activity_id)
        if not result:
            raise ActivityNotFoundException()

        activity, detail = result

        if activity.owner_id != command.owner_id:
            raise ForbiddenException("Solo el organizador puede publicar la actividad.")

        missing_fields: list[str] = []

        if not activity.name or not activity.name.strip():
            missing_fields.append("título")

        now = datetime.now(timezone.utc)
        act_date = activity.date
        if act_date.tzinfo is None:
            act_date = act_date.replace(tzinfo=timezone.utc)
        if act_date <= now:
            missing_fields.append("fecha futura válida")

        if not activity.image_url or not activity.image_url.strip():
            missing_fields.append("foto de portada")

        if not activity.capacity or activity.capacity <= 0:
            missing_fields.append("cupos disponibles")

        if not detail or detail.latitude is None or detail.longitude is None:
            missing_fields.append("ubicación en el mapa")

        if not detail or not detail.description or not detail.description.strip():
            missing_fields.append("descripción")

        if missing_fields:
            fields_str = ", ".join(missing_fields)
            raise ValidationException(
                f"No se puede publicar la actividad. Faltan completar los siguientes requisitos: {fields_str}."
            )

        activity.publish()
        self.activity_repository.save(activity)
        self.uow.commit()
        return activity
