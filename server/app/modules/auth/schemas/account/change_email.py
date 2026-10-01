from pydantic import EmailStr, field_validator
from sqlmodel import SQLModel

from app.core.config import settings


class RequestChangeEmailOtpResponse(SQLModel):
    """Response after requesting OTP for email change."""

    message: str
    expires_in_seconds: int


class VerifyChangeEmailOtpRequest(SQLModel):
    """Input payload to verify OTP for email change."""

    otp: str

    @field_validator("otp")
    @classmethod
    def validate_otp_length(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) != settings.OTP_LENGTH:
            raise ValueError(f"El codigo OTP debe tener {settings.OTP_LENGTH} digitos")
        return normalized


class VerifyChangeEmailOtpResponse(SQLModel):
    """Response after OTP verification for email change."""

    message: str
    email_change_token: str
    expires_in_seconds: int


class ChangeEmailRequest(SQLModel):
    """Input payload to update email with verification token."""

    new_email: EmailStr
    email_change_token: str
