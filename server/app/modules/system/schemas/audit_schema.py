from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel

from app.modules.system.models import AuditAction, AuditStatus


class RequestAuditAccessResponse(SQLModel):
    message: str
    expires_in_seconds: int


class VerifyAuditAccessRequest(SQLModel):
    access_key: str


class VerifyAuditAccessResponse(SQLModel):
    message: str
    session_expires_in_seconds: int


class AuditLogRead(SQLModel):
    id: UUID
    created_date: datetime
    action: AuditAction
    status: AuditStatus
    actor_user_id: UUID | None
    actor_identifier: str | None
    description: str
    ip: str


class PaginatedAuditLog(SQLModel):
    logs: list[AuditLogRead]
    page: int
    per_page: int
    total_pages: int
    has_prev: bool
    has_next: bool
