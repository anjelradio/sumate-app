from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)


@dataclass(frozen=True, slots=True)
class ListMyActivitiesQuery:
    current_user_id: str


@dataclass(frozen=True, slots=True)
class MyActivityListItemDTO:
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    capacity: int
    status: str
    registered_count: int
    creator_name: str | None = None
    creator_image: str | None = None


@dataclass(frozen=True, slots=True)
class MyActivityListDTO:
    items: tuple[MyActivityListItemDTO, ...]


class ListMyActivitiesQueryHandler:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository

    def execute(self, query: ListMyActivitiesQuery) -> MyActivityListDTO:
        results = self.activity_repository.list_my_activities(
            owner_id=query.current_user_id,
        )
        items = tuple(
            MyActivityListItemDTO(
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
                registered_count=registered_count,
                creator_name=activity.creator_name,
                creator_image=activity.creator_image,
            )
            for activity, registered_count in results
        )
        return MyActivityListDTO(items=items)
