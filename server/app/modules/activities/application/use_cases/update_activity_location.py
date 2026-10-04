from dataclasses import dataclass
from uuid import UUID

from app.core.integrations.nominatim import reverse_geocode
from app.modules.activities.domain.entities.activity_detail import ActivityDetail
from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.shared.application.ports import UnitOfWork
from app.shared.domain.exceptions import ForbiddenException


@dataclass(slots=True)
class UpdateActivityLocationCommand:
    activity_id: UUID
    owner_id: str
    latitude: float
    longitude: float
    place: str | None = None


class UpdateActivityLocationUseCase:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        uow: UnitOfWork,
    ) -> None:
        self.activity_repository = activity_repository
        self.uow = uow

    async def execute(self, command: UpdateActivityLocationCommand) -> ActivityDetail:
        activity = self.activity_repository.get_by_id(command.activity_id)
        if not activity:
            raise ActivityNotFoundException()

        if activity.owner_id != command.owner_id:
            raise ForbiddenException("Solo el organizador puede editar la ubicación.")

        _, address = await reverse_geocode(command.latitude, command.longitude)

        place = (command.place or "").strip()
        if not place:
            place = "Ubicación por definir"

        detail = self.activity_repository.get_detail_record(command.activity_id)
        if detail is None:
            detail = ActivityDetail.create(
                activity_id=command.activity_id,
                latitude=command.latitude,
                longitude=command.longitude,
                place=place,
                address=address,
            )
        else:
            detail.update_location(
                latitude=command.latitude,
                longitude=command.longitude,
                place=place,
                address=address,
            )

        self.activity_repository.save_detail(detail)
        self.uow.commit()
        return detail
