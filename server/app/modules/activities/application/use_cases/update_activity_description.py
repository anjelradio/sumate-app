from dataclasses import dataclass
from uuid import UUID

from app.modules.activities.domain.entities.activity_detail import ActivityDetail
from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.shared.application.ports import UnitOfWork
from app.shared.domain.exceptions import ForbiddenException


@dataclass(slots=True)
class UpdateActivityDescriptionCommand:
    activity_id: UUID
    owner_id: str
    description: str


class UpdateActivityDescriptionUseCase:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        uow: UnitOfWork,
    ) -> None:
        self.activity_repository = activity_repository
        self.uow = uow

    def execute(self, command: UpdateActivityDescriptionCommand) -> ActivityDetail:
        activity = self.activity_repository.get_by_id(command.activity_id)
        if not activity:
            raise ActivityNotFoundException()

        if activity.owner_id != command.owner_id:
            raise ForbiddenException("Solo el organizador puede editar la descripción.")

        detail = self.activity_repository.get_detail_record(command.activity_id)
        if detail is None:
            detail = ActivityDetail.create(
                activity_id=command.activity_id,
                description=command.description,
            )
        else:
            detail.update_description(command.description)

        self.activity_repository.save_detail(detail)
        self.uow.commit()
        return detail
