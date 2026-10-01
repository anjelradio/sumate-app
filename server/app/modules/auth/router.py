"""Module router that combines auth subrouters."""

from fastapi import APIRouter

from app.modules.auth.routers import account_router, auth_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(account_router)
