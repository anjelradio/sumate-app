from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID

from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)


@dataclass(frozen=True, slots=True)
class ActivityListItemDTO:
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    creator_name: str | None = None
    creator_image: str | None = None


@dataclass(frozen=True, slots=True)
class ActivityListDTO:
    items: tuple[ActivityListItemDTO, ...]


@dataclass(frozen=True, slots=True)
class ListExploreActivitiesQuery:
    current_user_id: str


class ListExploreActivitiesQueryHandler:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository

    def execute(self, query: ListExploreActivitiesQuery) -> ActivityListDTO:
        now = datetime.now(timezone.utc)
        activities = self.activity_repository.list_explore(
            exclude_owner_id=query.current_user_id,
            min_date=now,
        )

        items = tuple(
            ActivityListItemDTO(
                id=activity.id,
                name=activity.name,
                image_url=activity.image_url,
                date=activity.date,
                owner_id=activity.owner_id,
                capacity=activity.capacity,
                status=(
                    activity.status.value
                    if hasattr(activity.status, "value")
                    else str(activity.status)
                ),
                creator_name=activity.creator_name,
                creator_image=activity.creator_image,
            )
            for activity in activities
        )

        return ActivityListDTO(items=items)
