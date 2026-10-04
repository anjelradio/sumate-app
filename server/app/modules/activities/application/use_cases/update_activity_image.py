from dataclasses import dataclass
from uuid import UUID

from app.modules.activities.domain.entities.activity import Activity
from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.shared.application.ports import UnitOfWork
from app.shared.domain.exceptions import ForbiddenException


@dataclass(slots=True)
class UpdateActivityImageCommand:
    activity_id: UUID
    owner_id: str
    image_url: str


class UpdateActivityImageUseCase:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        uow: UnitOfWork,
    ) -> None:
        self.activity_repository = activity_repository
        self.uow = uow

    def execute(self, command: UpdateActivityImageCommand) -> Activity:
        activity = self.activity_repository.get_by_id(command.activity_id)
        if not activity:
            raise ActivityNotFoundException()

        if activity.owner_id != command.owner_id:
            raise ForbiddenException("Solo el organizador puede editar la imagen.")

        activity.update_image(command.image_url)
        self.activity_repository.save(activity)
        self.uow.commit()
        return activity
