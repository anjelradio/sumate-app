from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID

from app.modules.activities.domain.entities.activity import Activity
from app.modules.activities.domain.entities.activity_detail import ActivityDetail


class ActivityRepository(ABC):
    @abstractmethod
    def save(self, activity: Activity) -> None:
        ...

    @abstractmethod
    def get_by_id(self, activity_id: UUID) -> Activity | None:
        ...

    @abstractmethod
    def list_explore(
        self,
        *,
        exclude_owner_id: str,
        min_date: datetime,
    ) -> list[Activity]:
        ...

    @abstractmethod
    def list_my_activities(
        self,
        *,
        owner_id: str,
    ) -> list[tuple[Activity, int]]:
        ...

    @abstractmethod
    def save_detail(self, detail: ActivityDetail) -> None:
        ...

    @abstractmethod
    def get_detail_record(self, activity_id: UUID) -> ActivityDetail | None:
        ...

    @abstractmethod
    def get_detail_by_activity_id(
        self, activity_id: UUID
    ) -> tuple[Activity, ActivityDetail | None] | None:
        ...
