from uuid import UUID

from fastapi import HTTPException

from app.core.config import settings
from app.core.services import EmailTemplateService, OtpFlowService
from app.core.security.jwt import create_access_token, decode_token
from app.dependencies.auth import AuthenticatedUserContext
from app.dependencies.db import DBSession
from app.modules.auth.constants import INVALID_VERIFICATION_TOKEN, USER_NOT_FOUND
from app.modules.auth.repositories import UserRepository
from app.modules.auth.schemas import (
    ChangeEmailRequest,
    RequestChangeEmailOtpResponse,
    VerifyChangeEmailOtpRequest,
    VerifyChangeEmailOtpResponse,
)
from app.modules.system.models import AuditAction
from app.modules.system.service.audit_logger import AuditLogger


class ChangeEmailService:
    def __init__(self, db: DBSession):
        self.repo = UserRepository(db)
        self.audit_logger = AuditLogger(db)
        self.otp_flow = OtpFlowService("email_change")

    async def request_email_change_otp(
        self, user: AuthenticatedUserContext
    ) -> RequestChangeEmailOtpResponse:

        current_user = self.repo.get_by_id(user.id)
        if not current_user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

        otp_ttl_seconds = await self.otp_flow.request_otp(
            subject_id=str(user.id),
            destination_email=current_user.email,
            email_subject="Codigo OTP para cambio de correo",
            email_html=EmailTemplateService.build_otp_email("Codigo de verificacion"),
        )

        self.audit_logger.safe_log_system_success(
            action=AuditAction.ACCESS,
            description="Solicitud exitosa de OTP para cambio de correo",
            ip=user.ip,
            actor_user_id=user.id,
        )

        return RequestChangeEmailOtpResponse(
            message="Se envio un codigo OTP a tu correo actual",
            expires_in_seconds=otp_ttl_seconds,
        )

    def verify_email_change_otp(
        self, user: AuthenticatedUserContext, payload: VerifyChangeEmailOtpRequest
    ) -> VerifyChangeEmailOtpResponse:

        current_user = self.repo.get_by_id(user.id)
        if not current_user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

        self.otp_flow.verify_otp(
            subject_id=str(user.id),
            otp=payload.otp,
            expired_detail="El codigo OTP expiro o no fue solicitado",
            invalid_detail="Codigo OTP invalido",
        )

        token_ttl_seconds = settings.OTP_EXPIRES_MIN * 60
        email_change_token = create_access_token(
            {"sub": str(user.id), "purpose": "change_email"},
            minutes=settings.OTP_EXPIRES_MIN,
        )

        self.audit_logger.safe_log_system_success(
            action=AuditAction.ACCESS,
            description="Verificacion exitosa de OTP para cambio de correo",
            ip=user.ip,
            actor_user_id=user.id,
        )

        return VerifyChangeEmailOtpResponse(
            message="Codigo OTP verificado correctamente",
            email_change_token=email_change_token,
            expires_in_seconds=token_ttl_seconds,
        )

    def update_email(self, user: AuthenticatedUserContext, payload: ChangeEmailRequest):
        current_user = self.repo.get_by_id(user.id)
        if not current_user:
            raise HTTPException(status_code=404, detail=USER_NOT_FOUND)

        try:
            token_payload = decode_token(payload.email_change_token)
            token_user_id = UUID(token_payload.get("sub", ""))
            token_purpose = token_payload.get("purpose")
        except Exception:
            raise HTTPException(status_code=401, detail=INVALID_VERIFICATION_TOKEN)

        if token_purpose != "change_email" or token_user_id != user.id:
            raise HTTPException(status_code=403, detail=INVALID_VERIFICATION_TOKEN)

        new_email = str(payload.new_email).strip().lower()
        if new_email == current_user.email.lower():
            raise HTTPException(
                status_code=400,
                detail="El nuevo correo no puede ser igual al correo actual",
            )

        existing_user = self.repo.get_by_email(new_email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=409, detail="El correo ya esta en uso")

        current_user.email = new_email
        updated_user = self.repo.update(current_user)
        self.audit_logger.safe_log_system_success(
            action=AuditAction.UPDATE,
            description="Actualizacion exitosa de correo",
            ip=user.ip,
            actor_user_id=user.id,
        )

        return updated_user
