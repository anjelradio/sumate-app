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


class SQLModelActivityRepository(ActivityRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, activity_id: UUID) -> Activity | None:
        statement = select(ActivityModel).where(
            ActivityModel.id == activity_id,
            ActivityModel.deleted_date.is_(None),
        )
        record = self.db.exec(statement).first()
        return ActivityMapper.to_domain(record) if record else None

    def list_activities(
        self,
        *,
        owner_id: str | None = None,
        exclude_owner_id: str | None = None,
    ) -> list[Activity]:
        statement = select(ActivityModel).where(ActivityModel.deleted_date.is_(None))

        if owner_id:
            statement = statement.where(ActivityModel.owner_id == owner_id)
        elif exclude_owner_id:
            statement = statement.where(ActivityModel.owner_id != exclude_owner_id)

        # Ordenar por fecha de realización más próxima primero
        statement = statement.order_by(ActivityModel.date.asc())
        records = self.db.exec(statement).all()
        return [ActivityMapper.to_domain(record) for record in records]

    def save(self, activity: Activity) -> None:
        record = self.db.get(ActivityModel, activity.id)
        if record is None:
            model = ActivityMapper.to_model(activity)
            if not activity.is_active:
                model.deleted_date = datetime.now(timezone.utc)
            self.db.add(model)
            return

        record.name = activity.name
        record.owner_id = activity.owner_id
        record.image_url = activity.image_url
        record.date = activity.date

        if activity.is_active:
            record.deleted_date = None
        elif record.deleted_date is None:
            record.deleted_date = datetime.now(timezone.utc)

        record.modified_date = datetime.now(timezone.utc)
