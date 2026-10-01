from fastapi import HTTPException

from app.core.security.jwt import hash_password, verify_password
from app.core.validators import validate_password_policy
from app.dependencies.auth import AuthenticatedUserContext
from app.dependencies.db import DBSession
from app.modules.auth.constants import CURRENT_PASSWORD_INCORRECT, USER_NOT_FOUND
from app.modules.auth.repositories import UserRepository
from app.modules.auth.schemas import ChangePasswordRequest
from app.modules.system.models import AuditAction
from app.modules.system.service.audit_logger import AuditLogger


class ChangePasswordService:
    def __init__(self, db: DBSession):
        self.repo = UserRepository(db)
        self.audit_logger = AuditLogger(db)

    def update_password(
        self, user: AuthenticatedUserContext, payload: ChangePasswordRequest
    ) -> None:
        current_user = self.repo.get_by_id(user.id)
        if not current_user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

        if payload.new_password != payload.confirm_new_password:
            raise HTTPException(
                status_code=400,
                detail="La confirmacion de contrasena no coincide",
            )

        if not verify_password(payload.current_password[:72], current_user.hashed_password):
            raise HTTPException(status_code=401, detail=CURRENT_PASSWORD_INCORRECT)

        if payload.current_password == payload.new_password:
            raise HTTPException(
                status_code=400,
                detail="La nueva contrasena debe ser diferente a la actual",
            )

        validate_password_policy(payload.new_password)

        current_user.hashed_password = hash_password(payload.new_password)
        self.repo.update(current_user)
        self.audit_logger.safe_log_system_success(
            action=AuditAction.UPDATE,
            description="Actualizacion exitosa de contrasena",
            ip=user.ip,
            actor_user_id=user.id,
        )
