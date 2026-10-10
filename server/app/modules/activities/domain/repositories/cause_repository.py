from abc import ABC, abstractmethod
from uuid import UUID
from app.modules.activities.domain.entities.cause import Cause


class CauseRepository(ABC):
    @abstractmethod
    def list_all(self) -> list[Cause]:
        ...

    @abstractmethod
    def get_by_id(self, cause_id: UUID) -> Cause | None:
        ...

    @abstractmethod
    def get_by_slug(self, slug: str) -> Cause | None:
        ...

    @abstractmethod
    def get_by_ids(self, cause_ids: list[UUID]) -> list[Cause]:
        ...

    @abstractmethod
    def save(self, cause: Cause) -> None:
        ...
