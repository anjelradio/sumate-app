from app.shared.infrastructure.db.base_model import BaseModel
from sqlmodel import Field


class CauseModel(BaseModel, table=True):
    __tablename__ = "causes"

    name: str = Field(unique=True, index=True, nullable=False)
    slug: str = Field(unique=True, index=True, nullable=False)
