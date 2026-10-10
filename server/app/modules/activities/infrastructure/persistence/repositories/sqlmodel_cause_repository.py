from datetime import datetime, timezone
from uuid import UUID
from sqlmodel import Session, select

from app.modules.activities.domain.entities.cause import Cause
from app.modules.activities.domain.repositories.cause_repository import CauseRepository
from app.modules.activities.infrastructure.persistence.mappers.cause_mapper import (
    CauseMapper,
)
from app.modules.activities.infrastructure.persistence.models.cause_model import (
    CauseModel,
)


class SQLModelCauseRepository(CauseRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_all(self) -> list[Cause]:
        statement = (
            select(CauseModel)
            .where(CauseModel.deleted_date.is_(None))
            .order_by(CauseModel.name.asc())
        )
        records = self.db.exec(statement).all()
        return [CauseMapper.to_domain(record) for record in records]

    def get_by_id(self, cause_id: UUID) -> Cause | None:
        statement = select(CauseModel).where(
            CauseModel.id == cause_id,
            CauseModel.deleted_date.is_(None),
        )
        record = self.db.exec(statement).first()
        return CauseMapper.to_domain(record) if record else None

    def get_by_slug(self, slug: str) -> Cause | None:
        statement = select(CauseModel).where(
            CauseModel.slug == slug,
            CauseModel.deleted_date.is_(None),
        )
        record = self.db.exec(statement).first()
        return CauseMapper.to_domain(record) if record else None

    def get_by_ids(self, cause_ids: list[UUID]) -> list[Cause]:
        if not cause_ids:
            return []
        statement = select(CauseModel).where(
            CauseModel.id.in_(cause_ids),
            CauseModel.deleted_date.is_(None),
        )
        records = self.db.exec(statement).all()
        return [CauseMapper.to_domain(record) for record in records]

    def save(self, cause: Cause) -> None:
        record = self.db.get(CauseModel, cause.id)
        if record is None:
            model = CauseMapper.to_model(cause)
            self.db.add(model)
            return

        record.name = cause.name
        record.slug = cause.slug
        if cause.is_active:
            record.deleted_date = None
        elif record.deleted_date is None:
            record.deleted_date = datetime.now(timezone.utc)
        record.modified_date = datetime.now(timezone.utc)
