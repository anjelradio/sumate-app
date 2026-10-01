"""
    Barrel for routes, you can use this barrel file for the main file.
    Just import this file in the main.py :)
"""

from fastapi import APIRouter

from app.modules.auth.router import router as auth_router
from app.modules.system.router import router as system_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(system_router)
