from fastapi import APIRouter, Query

from app.dependencies import CurrentUser, DBSession
from app.modules.system.models import AuditAction, AuditStatus
from app.modules.system.schemas import (
    PaginatedAuditLog,
    RequestAuditAccessResponse,
    VerifyAuditAccessRequest,
    VerifyAuditAccessResponse,
)
from app.modules.system.service import AuditService

router = APIRouter(prefix="/system", tags=["Sistema"])


@router.post("/audit/access/request", response_model=RequestAuditAccessResponse)
async def request_audit_access_key(db: DBSession, user: CurrentUser):
    service = AuditService(db)
    return await service.request_access_key(user.user)


@router.post("/audit/access/verify", response_model=VerifyAuditAccessResponse)
def verify_audit_access_key(
    db: DBSession, payload: VerifyAuditAccessRequest, user: CurrentUser
):
    service = AuditService(db)
    return service.verify_access_key(user.user, payload.access_key)


@router.get("/audit/logs", response_model=PaginatedAuditLog)
def list_audit_logs(
    db: DBSession,
    user: CurrentUser,
    per_page: int = Query(default=8, ge=1, le=50),
    page: int = Query(default=1, ge=1),
    action: AuditAction | None = None,
    status: AuditStatus | None = None,
):
    service = AuditService(db)
    return service.list_logs(
        user=user.user,
        per_page=per_page,
        page=page,
        action=action,
        status=status,
    )
