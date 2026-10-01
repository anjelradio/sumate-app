from app.core.config import settings


class EmailTemplateService:
    @staticmethod
    def build_otp_email(title: str, otp_placeholder: str = "{otp}") -> str:
        return (
            f"<h2>{title}</h2>"
            f"<p>Tu codigo OTP es: <strong>{otp_placeholder}</strong></p>"
            f"<p>Este codigo expira en {settings.OTP_EXPIRES_MIN} minutos.</p>"
        )

    @staticmethod
    def build_temporary_password_email(temporary_password: str) -> str:
        return (
            "<h2>Nueva contrasena temporal</h2>"
            f"<p>Tu nueva contrasena es: <strong>{temporary_password}</strong></p>"
            "<p>Por seguridad, cambiala desde tu perfil despues de iniciar sesion.</p>"
        )
