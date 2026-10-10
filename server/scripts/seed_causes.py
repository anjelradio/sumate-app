import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.database import engine
from app.modules.activities.domain.entities.cause import Cause
from app.modules.activities.infrastructure.persistence.repositories.sqlmodel_cause_repository import (
    SQLModelCauseRepository,
)
from sqlmodel import Session

PREDEFINED_CAUSES = [
    {"name": "Salud", "slug": "salud"},
    {"name": "Animales", "slug": "animales"},
    {"name": "Medio Ambiente", "slug": "medio-ambiente"},
    {"name": "Educación", "slug": "educacion"},
    {"name": "Comunidad", "slug": "comunidad"},
    {"name": "Deporte", "slug": "deporte"},
    {"name": "Cultura y Arte", "slug": "cultura-y-arte"},
    {"name": "Niñez y Juventud", "slug": "ninez-y-juventud"},
    {"name": "Adulto Mayor", "slug": "adulto-mayor"},
    {"name": "Tecnología Social", "slug": "tecnologia-social"},
]


def seed_causes() -> None:
    with Session(engine) as session:
        repository = SQLModelCauseRepository(session)
        created_count = 0
        for item in PREDEFINED_CAUSES:
            existing = repository.get_by_slug(item["slug"])
            if existing is None:
                cause = Cause.create(name=item["name"], slug=item["slug"])
                repository.save(cause)
                created_count += 1
        session.commit()
        print(f"Seeding completed. Inserted {created_count} causes.")


if __name__ == "__main__":
    seed_causes()
