from enum import Enum
from uuid import UUID

from sqlmodel import Field

from app.common.models import UUIDBaseModel


class AuditAction(str, Enum):
    LOGIN = "login"
    LOGOUT = "logout"
    REGISTER = "register"
    JOIN = "join"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ACCESS = "access"
    INVITE = "invite"
    ROLE_CHANGE = "role_change"


class AuditStatus(str, Enum):
    SUCCESS = "success"
    FAILED = "failed"


class AuditLog(UUIDBaseModel, table=True):
    __tablename__ = "audit_logs"

    action: AuditAction = Field(index=True)
    status: AuditStatus = Field(index=True)

    actor_user_id: UUID | None = Field(default=None, index=True)
    actor_identifier_enc: str | None = Field(default=None, max_length=500)

    description_enc: str = Field(max_length=2000)
    ip_enc: str = Field(max_length=500)
