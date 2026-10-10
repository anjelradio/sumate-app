from app.modules.activities.domain.entities.cause import Cause
from app.modules.activities.infrastructure.persistence.models.cause_model import CauseModel


class CauseMapper:
    @staticmethod
    def to_domain(model: CauseModel) -> Cause:
        return Cause(
            id=model.id,
            name=model.name,
            slug=model.slug,
            is_active=model.deleted_date is None,
        )

    @staticmethod
    def to_model(entity: Cause) -> CauseModel:
        return CauseModel(
            id=entity.id,
            name=entity.name,
            slug=entity.slug,
        )
