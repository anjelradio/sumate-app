"""
app/modules/activities/application/queries/list_activities.py

Consulta para listar actividades según ámbito (propias del usuario o de otros miembros).
Devuelve DTOs inmutables de Python puro.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Literal
from uuid import UUID

from app.modules.activities.domain.repositories.activity_repository import ActivityRepository


@dataclass(frozen=True, slots=True)
class ListActivitiesQuery:
    scope: Literal["mine", "others"]
    current_user_id: str


@dataclass(frozen=True, slots=True)
class ActivityListItemDTO:
    id: UUID
    name: str
    image_url: str
    date: datetime
    owner_id: str
    creator_name: str | None = None


@dataclass(frozen=True, slots=True)
class ActivityListDTO:
    items: tuple[ActivityListItemDTO, ...]


class ListActivitiesQueryHandler:
    def __init__(self, activity_repository: ActivityRepository) -> None:
        self.activity_repository = activity_repository

    def execute(self, query: ListActivitiesQuery) -> ActivityListDTO:
        if query.scope == "mine":
            activities = self.activity_repository.list_activities(owner_id=query.current_user_id)
        else:
            activities = self.activity_repository.list_activities(exclude_owner_id=query.current_user_id)

        items = tuple(
            ActivityListItemDTO(
                id=activity.id,
                name=activity.name,
                image_url=activity.image_url,
                date=activity.date,
                owner_id=activity.owner_id,
                creator_name=None,
            )
            for activity in activities
        )

        return ActivityListDTO(items=items)
