from uuid import UUID
from sqlmodel import Field, SQLModel


class CauseRead(SQLModel):
    id: UUID
    name: str
    slug: str


class CauseListRead(SQLModel):
    items: list[CauseRead]


class ReplaceActivityCausesRequest(SQLModel):
    cause_ids: list[UUID] = Field(default_factory=list)
