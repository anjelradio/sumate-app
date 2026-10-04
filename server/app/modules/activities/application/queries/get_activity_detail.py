from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)


@dataclass(frozen=True, slots=True)
class GetActivityDetailQuery:
    activity_id: UUID
    current_user_id: str | None = None


@dataclass(frozen=True, slots=True)
class ActivityDetailDataDTO:
    id: UUID
    activity_id: UUID
    latitude: float | None = None
    longitude: float | None = None
    place: str | None = None
    address: str | None = None
    description: str | None = None


@dataclass(frozen=True, slots=True)
class ActivityDetailDTO:
    id: UUID
    name: str
    owner_id: str
    image_url: str
    date: datetime
    capacity: int
    status: str
    creator_name: str | None = None
    creator_image: str | None = None
    detail: ActivityDetailDataDTO | None = None


class GetActivityDetailQueryHandler:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository

    def execute(self, query: GetActivityDetailQuery) -> ActivityDetailDTO:
        result = self.activity_repository.get_detail_by_activity_id(query.activity_id)
        if not result:
            raise ActivityNotFoundException()

        activity, detail = result
        activity_status = (
            activity.status.value
            if hasattr(activity.status, "value")
            else str(activity.status)
        )

        if activity_status == "draft" and activity.owner_id != query.current_user_id:
            raise ActivityNotFoundException()

        detail_dto = (
            ActivityDetailDataDTO(
                id=detail.id,
                activity_id=detail.activity_id,
                latitude=detail.latitude,
                longitude=detail.longitude,
                place=detail.place,
                address=detail.address,
                description=detail.description,
            )
            if detail
            else None
        )

        return ActivityDetailDTO(
            id=activity.id,
            name=activity.name,
            owner_id=activity.owner_id,
            image_url=activity.image_url,
            date=activity.date,
            capacity=activity.capacity,
            status=activity_status,
            creator_name=activity.creator_name,
            creator_image=activity.creator_image,
            detail=detail_dto,
        )
