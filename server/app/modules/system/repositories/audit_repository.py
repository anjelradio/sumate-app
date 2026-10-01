from sqlmodel import Session, func, select

from app.modules.system.models import AuditAction, AuditLog, AuditStatus


class AuditRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, audit_log: AuditLog) -> AuditLog:
        self.db.add(audit_log)
        return audit_log

    def count_filtered(
        self,
        action: AuditAction | None = None,
        status: AuditStatus | None = None,
    ) -> int:
        query = select(func.count()).select_from(AuditLog).where(AuditLog.state)

        if action:
            query = query.where(AuditLog.action == action)
        if status:
            query = query.where(AuditLog.status == status)

        return self.db.exec(query).one()

    def list_filtered_paginated(
        self,
        per_page: int,
        page: int,
        action: AuditAction | None = None,
        status: AuditStatus | None = None,
    ) -> list[AuditLog]:
        offset = (page - 1) * per_page
        query = (
            select(AuditLog)
            .where(AuditLog.state)
            .order_by(AuditLog.created_date.desc())
            .offset(offset)
            .limit(per_page)
        )

        if action:
            query = query.where(AuditLog.action == action)
        if status:
            query = query.where(AuditLog.status == status)

        return self.db.exec(query).all()
