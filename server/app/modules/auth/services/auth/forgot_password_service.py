import string
from random import SystemRandom
from secrets import choice

from fastapi import HTTPException

from app.core.config import settings
from app.core.integrations import send_email
from app.core.services import EmailTemplateService, OtpFlowService
from app.core.security import hash_password
from app.core.validators import validate_password_policy
from app.dependencies.auth import UserContext
from app.dependencies.db import DBSession
from app.modules.auth.constants import INVALID_OR_EXPIRED_OTP
from app.modules.auth.repositories import UserRepository
from app.modules.auth.schemas import (
    RequestPasswordResetOtpRequest,
    RequestPasswordResetOtpResponse,
    VerifyPasswordResetOtpRequest,
    VerifyPasswordResetOtpResponse,
)
from app.modules.system.models import AuditAction
from app.modules.system.service.audit_logger import AuditLogger

secure_random = SystemRandom()


class ForgotPasswordService:
    def __init__(self, db: DBSession):
        self.repo = UserRepository(db)
        self.audit_logger = AuditLogger(db)
        self.otp_flow = OtpFlowService("password_reset")

    @staticmethod
    def _generate_temporary_password(length: int = 10) -> str:
        generated = [choice(string.ascii_uppercase) for _ in range(2)]
        generated.extend(choice(string.digits) for _ in range(2))

        pool = string.ascii_letters + string.digits
        for _ in range(max(length - 4, 4)):
            generated.append(choice(pool))

        secure_random.shuffle(generated)
        return "".join(generated)

    async def request_password_reset_otp(
        self,
        payload: RequestPasswordResetOtpRequest,
        request_user: UserContext,
    ) -> RequestPasswordResetOtpResponse:

        email = str(payload.email).strip().lower()
        user = self.repo.get_by_email(email)

        cooldown_ttl = self.otp_flow.get_cooldown_ttl(email)
        if cooldown_ttl > 0:
            raise HTTPException(
                status_code=429,
                detail=f"Debes esperar {cooldown_ttl} segundos para solicitar otro codigo",
            )

        otp_ttl_seconds = settings.OTP_EXPIRES_MIN * 60

        if user:
            otp_ttl_seconds = await self.otp_flow.request_otp(
                subject_id=email,
                destination_email=user.email,
                email_subject="Codigo OTP para recuperar contrasena",
                email_html=EmailTemplateService.build_otp_email(
                    "Recuperacion de contrasena"
                ),
            )

        self.audit_logger.safe_log_system_success(
            action=AuditAction.ACCESS,
            description="Solicitud exitosa de OTP para recuperacion de contrasena",
            ip=request_user.ip,
            actor_user_id=user.id if user else None,
        )

        return RequestPasswordResetOtpResponse(
            message="Si el correo existe, se envio un codigo OTP",
            expires_in_seconds=otp_ttl_seconds,
        )

    async def verify_password_reset_otp(
        self,
        payload: VerifyPasswordResetOtpRequest,
        request_user: UserContext,
    ) -> VerifyPasswordResetOtpResponse:

        email = str(payload.email).strip().lower()
        user = self.repo.get_by_email(email)
        if not user:
            raise HTTPException(status_code=400, detail=INVALID_OR_EXPIRED_OTP)

        self.otp_flow.verify_otp(
            subject_id=email,
            otp=payload.otp,
            expired_detail=INVALID_OR_EXPIRED_OTP,
            invalid_detail=INVALID_OR_EXPIRED_OTP,
        )

        temporary_password = self._generate_temporary_password()
        validate_password_policy(temporary_password)

        html_content = EmailTemplateService.build_temporary_password_email(
            temporary_password
        )

        try:
            await send_email(
                to_email=user.email,
                subject="Nueva contrasena temporal",
                html_content=html_content,
            )
        except Exception:
            raise HTTPException(
                status_code=500,
                detail="No se pudo enviar la nueva contrasena al correo",
            )

        user.hashed_password = hash_password(temporary_password)
        self.repo.update(user)

        self.audit_logger.safe_log_system_success(
            action=AuditAction.UPDATE,
            description="Restablecimiento exitoso de contrasena con OTP",
            ip=request_user.ip,
            actor_user_id=user.id,
        )

        return VerifyPasswordResetOtpResponse(
            message="Se envio una nueva contrasena a tu correo"
        )
