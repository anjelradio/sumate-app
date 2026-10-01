"""
    Barrel for models, you can use this barrel file for alembic.
    Just import this file in your env.py :)
    Register here all models that should be included in migrations.
"""

from app.modules.auth.models.user import User  # noqa: F401
from app.modules.system.models.audit_log import AuditLog  # noqa: F401
