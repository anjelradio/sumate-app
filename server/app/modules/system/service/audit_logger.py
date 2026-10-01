from uuid import UUID

from app.core.config import settings
from app.dependencies.db import DBSession
from app.modules.system.models import AuditAction, AuditStatus
from app.modules.system.service.audit_service import AuditService


class AuditLogger:
    def __init__(self, db: DBSession):
        self.db = db
        self.enabled = settings.AUDIT_ENABLED
        self.audit = AuditService(db) if self.enabled else None

    def safe_log(
        self,
        action: AuditAction,
        status: AuditStatus,
        description: str,
        ip: str,
        actor_user_id: UUID | None = None,
        actor_identifier: str | None = None,
    ) -> None:
        if not self.enabled or not self.audit:
            return

        try:
            self.audit.log_event(
                action=action,
                status=status,
                description=description,
                ip=ip,
                actor_user_id=actor_user_id,
                actor_identifier=actor_identifier,
            )
        except Exception:
            self.db.rollback()

    def safe_log_system_success(
        self,
        action: AuditAction,
        description: str,
        ip: str,
        actor_user_id: UUID | None = None,
        actor_identifier: str | None = None,
    ) -> None:
        self.safe_log(
            action=action,
            status=AuditStatus.SUCCESS,
            description=description,
            ip=ip,
            actor_user_id=actor_user_id,
            actor_identifier=actor_identifier,
        )

    def safe_log_system_failed(
        self,
        action: AuditAction,
        description: str,
        ip: str,
        actor_user_id: UUID | None = None,
        actor_identifier: str | None = None,
    ) -> None:
        self.safe_log(
            action=action,
            status=AuditStatus.FAILED,
            description=description,
            ip=ip,
            actor_user_id=actor_user_id,
            actor_identifier=actor_identifier,
        )
