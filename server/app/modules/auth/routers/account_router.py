from fastapi import APIRouter

from app.dependencies import CurrentUser, DBSession
from app.modules.auth.schemas import (
    ChangeEmailRequest,
    ChangePasswordRequest,
    RequestChangeEmailOtpResponse,
    UpdateProfileRequest,
    UserRead,
    VerifyChangeEmailOtpRequest,
    VerifyChangeEmailOtpResponse,
)
from app.modules.auth.services import (
    ChangeEmailService,
    ChangePasswordService,
    ChangeProfileService,
)

router = APIRouter(prefix="/auth/account", tags=["account"])


@router.patch("/profile", response_model=UserRead)
def update_profile(db: DBSession, user: CurrentUser, payload: UpdateProfileRequest):
    service = ChangeProfileService(db)
    return service.update_profile(user, payload)


@router.post("/email/request-otp", response_model=RequestChangeEmailOtpResponse)
async def request_email_change_otp(db: DBSession, user: CurrentUser):
    service = ChangeEmailService(db)
    return await service.request_email_change_otp(user)


@router.post("/email/verify-otp", response_model=VerifyChangeEmailOtpResponse)
def verify_email_change_otp(
    db: DBSession,
    user: CurrentUser,
    payload: VerifyChangeEmailOtpRequest,
):
    service = ChangeEmailService(db)
    return service.verify_email_change_otp(user, payload)


@router.patch("/email", response_model=UserRead)
def update_email(db: DBSession, user: CurrentUser, payload: ChangeEmailRequest):
    service = ChangeEmailService(db)
    return service.update_email(user, payload)


@router.patch("/password")
def update_password(db: DBSession, user: CurrentUser, payload: ChangePasswordRequest):
    service = ChangePasswordService(db)
    service.update_password(user, payload)
    return {"message": "Contrasena actualizada correctamente"}
