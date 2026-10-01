from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies import CurrentUser, DBSession, UserContext
from app.dependencies.auth import oauth2_scheme
from app.modules.auth.schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    RequestPasswordResetOtpRequest,
    RequestPasswordResetOtpResponse,
    VerifyPasswordResetOtpRequest,
    VerifyPasswordResetOtpResponse,
)
from app.modules.auth.services import AuthService, ForgotPasswordService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register", response_model=LoginResponse, status_code=status.HTTP_201_CREATED
)
def register(db: DBSession, payload: RegisterRequest, user: UserContext):
    service = AuthService(db)
    token, created_user = service.register_with_token(payload, user)
    return {"user": created_user, "access_token": token}


@router.post("/login", response_model=LoginResponse)
def login(db: DBSession, payload: LoginRequest, user: UserContext):
    service = AuthService(db)
    token, user = service.login(payload.email, payload.password, user)
    return {"user": user, "access_token": token}


@router.post("/token", response_model=LoginResponse)
def token_login(
    db: DBSession,
    user: UserContext,
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    service = AuthService(db)
    token, user = service.login(form.username, form.password, user)
    return {"user": user, "access_token": token}


@router.post("/check-status", response_model=LoginResponse)
def check_status(user: CurrentUser, token: str = Depends(oauth2_scheme)):
    return {"user": user.user, "access_token": token}


@router.post(
    "/forgot-password/request-otp", response_model=RequestPasswordResetOtpResponse
)
async def request_password_reset_otp(
    db: DBSession,
    payload: RequestPasswordResetOtpRequest,
    user: UserContext,
):
    service = ForgotPasswordService(db)
    return await service.request_password_reset_otp(payload, user)


@router.post(
    "/forgot-password/verify-otp", response_model=VerifyPasswordResetOtpResponse
)
async def verify_password_reset_otp(
    db: DBSession,
    payload: VerifyPasswordResetOtpRequest,
    user: UserContext,
):
    service = ForgotPasswordService(db)
    return await service.verify_password_reset_otp(payload, user)
