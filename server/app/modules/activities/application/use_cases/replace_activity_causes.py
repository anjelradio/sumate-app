from dataclasses import dataclass
from uuid import UUID

from app.modules.activities.domain.entities.activity import ActivityStatus
from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.modules.activities.domain.repositories.cause_repository import (
    CauseRepository,
)
from app.shared.application.ports import UnitOfWork
from app.shared.domain.exceptions import ForbiddenException, ValidationException


@dataclass(slots=True)
class ReplaceActivityCausesCommand:
    activity_id: UUID
    owner_id: str
    cause_ids: list[UUID]


class ReplaceActivityCausesUseCase:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        cause_repository: CauseRepository,
        uow: UnitOfWork,
    ) -> None:
        self.activity_repository = activity_repository
        self.cause_repository = cause_repository
        self.uow = uow

    def execute(self, command: ReplaceActivityCausesCommand) -> None:
        activity = self.activity_repository.get_by_id(
            command.activity_id, for_update=True
        )
        if activity is None:
            raise ActivityNotFoundException()

        if activity.owner_id != command.owner_id:
            raise ForbiddenException("Solo el organizador puede modificar las causas.")

        if activity.status == ActivityStatus.ACTIVE and not command.cause_ids:
            raise ValidationException(
                "Una actividad publicada debe mantener al menos una causa asignada."
            )

        unique_cause_ids = list(dict.fromkeys(command.cause_ids))
        if unique_cause_ids:
            valid_causes = self.cause_repository.get_by_ids(unique_cause_ids)
            if len(valid_causes) != len(unique_cause_ids):
                raise ValidationException(
                    "Una o más causas seleccionadas no existen en el catálogo."
                )

        self.activity_repository.replace_activity_causes(
            activity.id, unique_cause_ids
        )
        self.uow.commit()
