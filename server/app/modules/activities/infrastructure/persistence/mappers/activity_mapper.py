"""
app/modules/activities/infrastructure/persistence/mappers/activity_mapper.py

Traductor puro bidireccional entre la entidad Activity y el modelo ActivityModel.
"""

from app.modules.activities.domain.entities.activity import Activity
from app.modules.activities.infrastructure.persistence.models.activity_model import ActivityModel


class ActivityMapper:
    """Mapeo entre entidad de dominio Activity y modelo de persistencia ActivityModel."""

    @staticmethod
    def to_domain(model: ActivityModel) -> Activity:
        return Activity(
            id=model.id,
            name=model.name,
            owner_id=model.owner_id,
            image_url=model.image_url,
            date=model.date,
            is_active=model.deleted_date is None,
        )

    @staticmethod
    def to_model(entity: Activity) -> ActivityModel:
        return ActivityModel(
            id=entity.id,
            name=entity.name,
            owner_id=entity.owner_id,
            image_url=entity.image_url,
            date=entity.date,
        )
