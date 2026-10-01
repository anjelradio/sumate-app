from fastapi import HTTPException

from app.core.security.jwt import create_access_token, hash_password, verify_password
from app.core.validators import validate_password_policy
from app.dependencies.auth import UserContext
from app.dependencies.db import DBSession
from app.modules.auth.constants import (
    AUDIT_LOGIN_FAILED,
    AUDIT_LOGIN_SUCCESS,
    AUDIT_REGISTER_FAILED,
    AUDIT_REGISTER_SUCCESS,
)
from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository
from app.modules.auth.schemas import RegisterRequest
from app.modules.system.models import AuditAction
from app.modules.system.service.audit_logger import AuditLogger


class AuthService:
    def __init__(self, db: DBSession):
        self.repo = UserRepository(db)
        self.audit_logger = AuditLogger(db)

    def register(self, payload: RegisterRequest, user: UserContext) -> User:
        if self.repo.get_by_email(payload.email):
            self.audit_logger.safe_log_system_failed(
                action=AuditAction.REGISTER,
                description=AUDIT_REGISTER_FAILED,
                ip=user.ip,
            )
            raise HTTPException(status_code=400, detail="Email ya registrado")

        validate_password_policy(payload.password)

        new_user = User(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            hashed_password=hash_password(payload.password),
            is_super_admin=payload.is_super_admin,
        )

        created_user = self.repo.create(new_user)
        self.audit_logger.safe_log_system_success(
            action=AuditAction.REGISTER,
            description=AUDIT_REGISTER_SUCCESS,
            ip=user.ip,
            actor_user_id=created_user.id,
        )

        return created_user

    def register_with_token(self, payload: RegisterRequest, request_user: UserContext):
        user = self.register(payload, request_user)
        token = create_access_token({"sub": str(user.id)})
        return token, user

    def login(self, email: str, password: str, request_user: UserContext):
        user = self.repo.get_by_email(email)
        if not user:
            self.audit_logger.safe_log_system_failed(
                action=AuditAction.LOGIN,
                description=AUDIT_LOGIN_FAILED,
                ip=request_user.ip,
            )
            raise HTTPException(status_code=401, detail="Credenciales Invalidas")

        if not verify_password(password[:72], user.hashed_password):
            self.audit_logger.safe_log_system_failed(
                action=AuditAction.LOGIN,
                description=f"Contrasena incorrecta para email {email}",
                ip=request_user.ip,
                actor_user_id=user.id,
            )
            raise HTTPException(status_code=401, detail="Contrasena Incorrecta")

        token = create_access_token({"sub": str(user.id)})
        self.audit_logger.safe_log_system_success(
            action=AuditAction.LOGIN,
            description=AUDIT_LOGIN_SUCCESS,
            ip=request_user.ip,
            actor_user_id=user.id,
        )
        return token, user
