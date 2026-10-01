from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel

from app.core.config import settings


class RequestPasswordResetOtpRequest(SQLModel):
    """Input payload to request OTP for password reset."""

    email: EmailStr


class RequestPasswordResetOtpResponse(SQLModel):
    """Response after requesting OTP for password reset."""

    message: str
    expires_in_seconds: int


class VerifyPasswordResetOtpRequest(SQLModel):
    """Input payload to verify OTP and trigger temporary password reset."""

    email: EmailStr
    otp: str

    @field_validator("otp")
    @classmethod
    def validate_otp_length(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) != settings.OTP_LENGTH:
            raise ValueError(f"El codigo OTP debe tener {settings.OTP_LENGTH} digitos")
        return normalized


class VerifyPasswordResetOtpResponse(SQLModel):
    """Response after successful password reset OTP verification."""

    message: str
