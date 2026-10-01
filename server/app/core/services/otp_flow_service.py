from secrets import compare_digest

from fastapi import HTTPException

from app.core.config import settings
from app.core.integrations import redis_client, send_email
from app.core.security.otp import generate_otp, hash_otp


class OtpFlowService:
    def __init__(self, flow_name: str):
        self.flow_name = flow_name

    def _otp_key(self, subject_id: str) -> str:
        return f"{self.flow_name}_otp:{subject_id}"

    def _attempts_key(self, subject_id: str) -> str:
        return f"{self.flow_name}_otp_attempts:{subject_id}"

    def _cooldown_key(self, subject_id: str) -> str:
        return f"{self.flow_name}_otp_cooldown:{subject_id}"

    def get_cooldown_ttl(self, subject_id: str) -> int:
        ttl = redis_client.ttl(self._cooldown_key(subject_id))
        return ttl if ttl and ttl > 0 else 0

    async def request_otp(
        self,
        subject_id: str,
        destination_email: str,
        email_subject: str,
        email_html: str,
    ) -> int:
        cooldown_ttl = self.get_cooldown_ttl(subject_id)
        if cooldown_ttl > 0:
            raise HTTPException(
                status_code=429,
                detail=f"Debes esperar {cooldown_ttl} segundos para solicitar otro codigo",
            )

        otp = generate_otp()
        otp_hashed = hash_otp(otp)
        otp_ttl_seconds = settings.OTP_EXPIRES_MIN * 60

        try:
            await send_email(
                to_email=destination_email,
                subject=email_subject,
                html_content=email_html.replace("{otp}", otp),
            )
        except Exception:
            raise HTTPException(status_code=500, detail="No se pudo enviar el codigo OTP")

        redis_client.set(self._otp_key(subject_id), otp_hashed, ex=otp_ttl_seconds)
        redis_client.set(self._attempts_key(subject_id), "0", ex=otp_ttl_seconds)
        redis_client.set(
            self._cooldown_key(subject_id), "1", ex=settings.OTP_RESEND_COOLDOWN_SEC
        )
        return otp_ttl_seconds

    def verify_otp(
        self,
        subject_id: str,
        otp: str,
        *,
        expired_detail: str,
        invalid_detail: str,
    ) -> None:
        otp_key = self._otp_key(subject_id)
        attempts_key = self._attempts_key(subject_id)
        cooldown_key = self._cooldown_key(subject_id)

        stored_otp_hash = redis_client.get(otp_key)
        if not stored_otp_hash:
            raise HTTPException(status_code=400, detail=expired_detail)

        attempts = int(redis_client.get(attempts_key) or "0")
        if attempts >= settings.OTP_MAX_ATTEMPTS:
            raise HTTPException(
                status_code=429,
                detail="Se alcanzo el limite de intentos para el codigo OTP",
            )

        provided_otp_hash = hash_otp(otp.strip())
        if not compare_digest(stored_otp_hash, provided_otp_hash):
            attempts += 1
            remaining_ttl = redis_client.ttl(otp_key)
            if remaining_ttl and remaining_ttl > 0:
                redis_client.set(attempts_key, str(attempts), ex=remaining_ttl)
            else:
                redis_client.set(attempts_key, str(attempts))

            if attempts >= settings.OTP_MAX_ATTEMPTS:
                raise HTTPException(
                    status_code=429,
                    detail="Se alcanzo el limite de intentos para el codigo OTP",
                )
            raise HTTPException(status_code=400, detail=invalid_detail)

        redis_client.delete(otp_key, attempts_key, cooldown_key)
