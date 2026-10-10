from __future__ import annotations
from uuid import UUID, uuid4


class Cause:
    def __init__(
        self,
        id: UUID,
        name: str,
        slug: str,
        is_active: bool = True,
    ) -> None:
        self.id = id
        self.name = self.normalize_name(name)
        self.slug = self.normalize_slug(slug)
        self.is_active = is_active

    @classmethod
    def create(cls, *, name: str, slug: str) -> Cause:
        return cls(id=uuid4(), name=name, slug=slug, is_active=True)

    @staticmethod
    def normalize_name(name: str) -> str:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("El nombre de la causa no puede estar vacío.")
        return name.strip()

    @staticmethod
    def normalize_slug(slug: str) -> str:
        if not isinstance(slug, str) or not slug.strip():
            raise ValueError("El slug de la causa no puede estar vacío.")
        return slug.strip().lower()
