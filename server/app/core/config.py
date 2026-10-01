from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Your project name :)"
    LANGUAGE_CODE: str = "es"
    TIME_ZONE: str = "America/La_Paz"

    # Environment DEV/PROD
    ENVIRONMENT: str = Field(..., env="ENVIRONMENT")

    # Database
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # JWT
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALG: str = Field(default="HS256", env="JWT_ALG")
    JWT_EXPIRES_MIN: int = Field(default=60 * 24, env="JWT_EXPIRES_MIN") # 1 day

    # Brevo Email Service
    BREVO_API_KEY: str = Field(default="", env="BREVO_API_KEY")
    BREVO_SENDER_EMAIL: str = Field(default="", env="BREVO_SENDER_EMAIL")
    BREVO_SENDER_NAME: str = Field(default="your-sender-name-here", env="BREVO_SENDER_NAME")

    # OTP code
    OTP_LENGTH: int = Field(default=6, env="OTP_LENGTH")
    OTP_EXPIRES_MIN: int = Field(default=5, env="OTP_EXPIRES_MIN")
    OTP_MAX_ATTEMPTS: int = Field(default=5, env="OTP_MAX_ATTEMPTS")
    OTP_RESEND_COOLDOWN_SEC: int = Field(default=60, env="OTP_RESEND_COOLDOWN_SEC")

    # Redis
    REDIS_URL: str = Field(..., env="REDIS_URL")

    # Audit config
    AUDIT_ENABLED: bool = Field(default=False, env="AUDIT_ENABLED")
    AUDIT_ENCRYPTION_KEY: str = Field(default="", env="AUDIT_ENCRYPTION_KEY")
    AUDIT_ACCESS_KEY_LENGTH: int = Field(default=10, env="AUDIT_ACCESS_KEY_LENGTH")
    AUDIT_ACCESS_EXPIRES_MIN: int = Field(default=10, env="AUDIT_ACCESS_EXPIRES_MIN")
    AUDIT_ACCESS_MAX_ATTEMPTS: int = Field(default=5, env="AUDIT_ACCESS_MAX_ATTEMPTS")
    AUDIT_ACCESS_SESSION_SEC: int = Field(default=1800, env="AUDIT_ACCESS_SESSION_SEC")

    class Config:
        env_file = ".env"


settings = Settings()
