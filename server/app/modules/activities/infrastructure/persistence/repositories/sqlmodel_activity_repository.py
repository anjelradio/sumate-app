"""
app/modules/activities/infrastructure/persistence/repositories/sqlmodel_activity_repository.py

Implementación de ActivityRepository utilizando SQLModel / SQLAlchemy Session.
Cumple con convenciones de nomenclatura, filtrado de deleted_date y métodos de persistencia.
"""

from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session, select

from app.modules.activities.domain.entities.activity import Activity
from app.modules.activities.domain.repositories.activity_repository import ActivityRepository
from app.modules.activities.infrastructure.persistence.mappers.activity_mapper import ActivityMapper
from app.modules.activities.infrastructure.persistence.models.activity_model import ActivityModel
from app.shared.infrastructure.db.better_auth import BetterAuthUser


class SQLModelActivityRepository(ActivityRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, activity_id: UUID) -> Activity | None:
        statement = (
            select(ActivityModel, BetterAuthUser.name.label("creator_name"))
            .outerjoin(BetterAuthUser, ActivityModel.owner_id == BetterAuthUser.id)
            .where(
                ActivityModel.id == activity_id,
                ActivityModel.deleted_date.is_(None),
            )
        )
        result = self.db.exec(statement).first()
        if not result:
            return None
        record, creator_name = result
        return ActivityMapper.to_domain(record, creator_name=creator_name)

    def list_activities(
        self,
        *,
        owner_id: str | None = None,
        exclude_owner_id: str | None = None,
    ) -> list[Activity]:
        statement = (
            select(ActivityModel, BetterAuthUser.name.label("creator_name"))
            .outerjoin(BetterAuthUser, ActivityModel.owner_id == BetterAuthUser.id)
            .where(ActivityModel.deleted_date.is_(None))
        )

        if owner_id:
            statement = statement.where(ActivityModel.owner_id == owner_id)
            # Para mis actividades: orden descendente por fecha de registro
            statement = statement.order_by(ActivityModel.created_date.desc())
        elif exclude_owner_id:
            statement = statement.where(
                ActivityModel.owner_id != exclude_owner_id,
                ActivityModel.status == "active",
            )
            # Para explorar: orden cronológico ascendente por fecha de realización
            statement = statement.order_by(ActivityModel.date.asc())

        results = self.db.exec(statement).all()
        return [
            ActivityMapper.to_domain(record, creator_name=creator_name)
            for record, creator_name in results
        ]

    def save(self, activity: Activity) -> None:
        record = self.db.get(ActivityModel, activity.id)
        if record is None:
            model = ActivityMapper.to_model(activity)
            self.db.add(model)
            return

        record.name = activity.name
        record.owner_id = activity.owner_id
        record.image_url = activity.image_url
        record.date = activity.date
        record.capacity = activity.capacity
        record.status = (
            activity.status.value
            if hasattr(activity.status, "value")
            else str(activity.status)
        )
        record.modified_date = datetime.now(timezone.utc)
