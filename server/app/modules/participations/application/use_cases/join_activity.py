from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.modules.participations.domain.entities.participation import Participation
from app.modules.participations.domain.exceptions import (
    ActivityCapacityExceededException,
    AlreadyParticipatingException,
    CannotJoinOwnActivityException,
    CannotJoinPastActivityException,
)
from app.modules.participations.domain.repositories.participation_repository import (
    ParticipationRepository,
)
from app.shared.application.ports import UnitOfWork


@dataclass(slots=True)
class JoinActivityCommand:
    activity_id: UUID
    user_id: str


class JoinActivityUseCase:
    def __init__(
        self,
        activity_repository: ActivityRepository,
        participation_repository: ParticipationRepository,
        uow: UnitOfWork,
    ) -> None:
        self.activity_repository = activity_repository
        self.participation_repository = participation_repository
        self.uow = uow

    def execute(self, command: JoinActivityCommand) -> Participation:
        activity = self.activity_repository.get_by_id(command.activity_id)
        if not activity:
            raise ActivityNotFoundException()

        if activity.owner_id == command.user_id:
            raise CannotJoinOwnActivityException()

        now = datetime.now(timezone.utc)
        act_date = (
            activity.date
            if activity.date.tzinfo
            else activity.date.replace(tzinfo=timezone.utc)
        )
        if act_date <= now:
            raise CannotJoinPastActivityException()

        if self.participation_repository.is_participating(
            command.activity_id, command.user_id
        ):
            raise AlreadyParticipatingException()

        current_count = self.participation_repository.count_by_activity_id(
            command.activity_id
        )
        if current_count >= activity.capacity:
            raise ActivityCapacityExceededException()

        participation = Participation.create(
            activity_id=command.activity_id,
            user_id=command.user_id,
        )
        self.participation_repository.save(participation)
        self.uow.commit()
        return participation
