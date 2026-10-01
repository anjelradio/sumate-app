from fastapi import HTTPException

from app.dependencies.auth import AuthenticatedUserContext
from app.dependencies.db import DBSession
from app.modules.auth.constants import USER_NOT_FOUND
from app.modules.auth.repositories import UserRepository
from app.modules.auth.schemas import UpdateProfileRequest
from app.modules.system.models import AuditAction
from app.modules.system.service.audit_logger import AuditLogger


class ChangeProfileService:
    def __init__(self, db: DBSession):
        self.repo = UserRepository(db)
        self.audit_logger = AuditLogger(db)

    def update_profile(self, user: AuthenticatedUserContext, payload: UpdateProfileRequest):
        current_user = self.repo.get_by_id(user.id)
        if not current_user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

        current_user.first_name = payload.first_name
        current_user.last_name = payload.last_name

        updated_user = self.repo.update(current_user)
        self.audit_logger.safe_log_system_success(
            action=AuditAction.UPDATE,
            description="Actualizacion exitosa de perfil",
            ip=user.ip,
            actor_user_id=user.id,
        )
        return updated_user
