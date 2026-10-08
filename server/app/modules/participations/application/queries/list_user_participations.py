from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from app.modules.participations.domain.repositories.participation_repository import (
    ParticipationRepository,
)


@dataclass(frozen=True, slots=True)
class ParticipatedActivityListItemDTO:
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    enrolled_date: datetime
    is_past: bool
    creator_name: str | None = None
    creator_image: str | None = None


@dataclass(frozen=True, slots=True)
class ListUserParticipationsQuery:
    user_id: str


@dataclass(frozen=True, slots=True)
class UserParticipationsDTO:
    items: list[ParticipatedActivityListItemDTO]


class ListUserParticipationsQueryHandler:
    def __init__(self, participation_repository: ParticipationRepository) -> None:
        self.participation_repository = participation_repository

    def execute(self, query: ListUserParticipationsQuery) -> UserParticipationsDTO:
        raw_items = self.participation_repository.list_user_participated_activities(
            query.user_id
        )
        now = datetime.now(timezone.utc)
        items: list[ParticipatedActivityListItemDTO] = []
        for part, act, enrolled_date, creator_name, creator_image in raw_items:
            act_date = act.date if act.date.tzinfo else act.date.replace(tzinfo=timezone.utc)
            is_past = act_date < now
            items.append(
                ParticipatedActivityListItemDTO(
                    id=act.id,
                    name=act.name,
                    image_url=act.image_url,
                    date=act_date,
                    owner_id=act.owner_id,
                    capacity=act.capacity,
                    status=act.status.value if hasattr(act.status, "value") else str(act.status),
                    enrolled_date=enrolled_date,
                    is_past=is_past,
                    creator_name=creator_name,
                    creator_image=creator_image,
                )
            )

        upcoming = sorted([item for item in items if not item.is_past], key=lambda x: x.date)
        past = sorted([item for item in items if item.is_past], key=lambda x: x.date, reverse=True)
        return UserParticipationsDTO(items=upcoming + past)
