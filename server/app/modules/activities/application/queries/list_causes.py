from dataclasses import dataclass
from uuid import UUID

from app.modules.activities.domain.repositories.cause_repository import CauseRepository


@dataclass(frozen=True, slots=True)
class CauseDTO:
    id: UUID
    name: str
    slug: str


@dataclass(frozen=True, slots=True)
class CauseListDTO:
    items: tuple[CauseDTO, ...]


@dataclass(frozen=True, slots=True)
class ListCausesQuery:
    pass


class ListCausesQueryHandler:
    def __init__(self, cause_repository: CauseRepository) -> None:
        self.cause_repository = cause_repository

    def execute(self, query: ListCausesQuery | None = None) -> CauseListDTO:
        causes = self.cause_repository.list_all()
        return CauseListDTO(
            items=tuple(
                CauseDTO(
                    id=c.id,
                    name=c.name,
                    slug=c.slug,
                )
                for c in causes
            )
        )
