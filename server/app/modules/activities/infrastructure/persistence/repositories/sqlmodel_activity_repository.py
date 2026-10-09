from datetime import datetime, timezone
from uuid import UUID

from app.modules.activities.domain.entities.activity import Activity
from app.modules.activities.domain.entities.activity_detail import ActivityDetail
from app.modules.activities.domain.repositories.activity_repository import (
    ActivityRepository,
)
from app.modules.activities.infrastructure.persistence.mappers.activity_detail_mapper import (
    ActivityDetailMapper,
)
from app.modules.activities.infrastructure.persistence.mappers.activity_mapper import (
    ActivityMapper,
)
from app.modules.activities.infrastructure.persistence.models.activity_detail_model import (
    ActivityDetailModel,
)
from app.modules.activities.infrastructure.persistence.models.activity_model import (
    ActivityModel,
)
from app.modules.participations.infrastructure.persistence.models.participation_model import (
    ParticipationModel,
)
from app.shared.infrastructure.db.better_auth import BetterAuthUser
from sqlalchemy import func
from sqlmodel import Session, select


class SQLModelActivityRepository(ActivityRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(
        self, activity_id: UUID, for_update: bool = False
    ) -> Activity | None:
        statement = (
            select(
                ActivityModel,
                BetterAuthUser.name.label("creator_name"),
                BetterAuthUser.image.label("creator_image"),
            )
            .outerjoin(BetterAuthUser, ActivityModel.owner_id == BetterAuthUser.id)
            .where(
                ActivityModel.id == activity_id,
                ActivityModel.deleted_date.is_(None),
            )
        )
        if for_update:
            statement = statement.with_for_update(of=ActivityModel)
        result = self.db.exec(statement).first()
        if not result:
            return None
        record, creator_name, creator_image = result
        return ActivityMapper.to_domain(
            record,
            creator_name=creator_name,
            creator_image=creator_image,
        )

    def list_explore(
        self,
        *,
        exclude_owner_id: str,
        min_date: datetime,
    ) -> list[Activity]:
        statement = (
            select(
                ActivityModel,
                BetterAuthUser.name.label("creator_name"),
                BetterAuthUser.image.label("creator_image"),
            )
            .outerjoin(BetterAuthUser, ActivityModel.owner_id == BetterAuthUser.id)
            .where(
                ActivityModel.deleted_date.is_(None),
                ActivityModel.owner_id != exclude_owner_id,
                ActivityModel.status == "active",
                ActivityModel.date >= min_date,
            )
            .order_by(ActivityModel.date.asc())
        )
        results = self.db.exec(statement).all()
        return [
            ActivityMapper.to_domain(
                record,
                creator_name=creator_name,
                creator_image=creator_image,
            )
            for record, creator_name, creator_image in results
        ]

    def list_my_activities(
        self,
        *,
        owner_id: str,
    ) -> list[tuple[Activity, int]]:
        subquery = (
            select(
                ParticipationModel.activity_id,
                func.count(ParticipationModel.id).label("registered_count"),
            )
            .where(ParticipationModel.deleted_date.is_(None))
            .group_by(ParticipationModel.activity_id)
            .subquery()
        )
        statement = (
            select(
                ActivityModel,
                BetterAuthUser.name.label("creator_name"),
                BetterAuthUser.image.label("creator_image"),
                func.coalesce(subquery.c.registered_count, 0).label("registered_count"),
            )
            .outerjoin(BetterAuthUser, ActivityModel.owner_id == BetterAuthUser.id)
            .outerjoin(subquery, ActivityModel.id == subquery.c.activity_id)
            .where(
                ActivityModel.owner_id == owner_id,
                ActivityModel.deleted_date.is_(None),
            )
            .order_by(ActivityModel.created_date.desc())
        )
        results = self.db.exec(statement).all()
        return [
            (
                ActivityMapper.to_domain(
                    record,
                    creator_name=creator_name,
                    creator_image=creator_image,
                ),
                int(reg_count),
            )
            for record, creator_name, creator_image, reg_count in results
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

    def save_detail(self, detail: ActivityDetail) -> None:
        statement = select(ActivityDetailModel).where(
            ActivityDetailModel.activity_id == detail.activity_id
        )
        record = self.db.exec(statement).first()
        if record is None:
            model = ActivityDetailMapper.to_model(detail)
            self.db.add(model)
            return

        record.latitude = detail.latitude
        record.longitude = detail.longitude
        record.place = detail.place
        record.address = detail.address
        record.description = detail.description
        record.modified_date = datetime.now(timezone.utc)

    def get_detail_record(self, activity_id: UUID) -> ActivityDetail | None:
        statement = select(ActivityDetailModel).where(
            ActivityDetailModel.activity_id == activity_id
        )
        record = self.db.exec(statement).first()
        if not record:
            return None
        return ActivityDetailMapper.to_domain(record)

    def get_detail_by_activity_id(
        self, activity_id: UUID
    ) -> tuple[Activity, ActivityDetail | None] | None:
        statement = (
            select(
                ActivityModel,
                BetterAuthUser.name.label("creator_name"),
                BetterAuthUser.image.label("creator_image"),
                ActivityDetailModel,
            )
            .outerjoin(BetterAuthUser, ActivityModel.owner_id == BetterAuthUser.id)
            .outerjoin(
                ActivityDetailModel,
                ActivityModel.id == ActivityDetailModel.activity_id,
            )
            .where(
                ActivityModel.id == activity_id,
                ActivityModel.deleted_date.is_(None),
            )
        )
        result = self.db.exec(statement).first()
        if not result:
            return None

        act_model, creator_name, creator_image, detail_model = result
        activity = ActivityMapper.to_domain(
            act_model,
            creator_name=creator_name,
            creator_image=creator_image,
        )
        detail = ActivityDetailMapper.to_domain(detail_model) if detail_model else None
        return (activity, detail)

    def delete(self, activity: Activity) -> None:
        statement_detail = select(ActivityDetailModel).where(
            ActivityDetailModel.activity_id == activity.id
        )
        detail_record = self.db.exec(statement_detail).first()
        if detail_record:
            self.db.delete(detail_record)

        record = self.db.get(ActivityModel, activity.id)
        if record:
            self.db.delete(record)
