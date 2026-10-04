from app.modules.activities.domain.entities.activity_detail import ActivityDetail
from app.modules.activities.infrastructure.persistence.models.activity_detail_model import ActivityDetailModel


class ActivityDetailMapper:
    @staticmethod
    def to_domain(model: ActivityDetailModel) -> ActivityDetail:
        return ActivityDetail(
            id=model.id,
            activity_id=model.activity_id,
            latitude=model.latitude,
            longitude=model.longitude,
            place=model.place,
            address=model.address,
            description=model.description,
        )

    @staticmethod
    def to_model(entity: ActivityDetail) -> ActivityDetailModel:
        return ActivityDetailModel(
            id=entity.id,
            activity_id=entity.activity_id,
            latitude=entity.latitude,
            longitude=entity.longitude,
            place=entity.place,
            address=entity.address,
            description=entity.description,
        )
