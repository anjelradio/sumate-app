from datetime import datetime, timezone
import pytest
from app.modules.activities.domain.entities.activity import Activity, ActivityStatus
from app.shared.infrastructure.db.base_model import BaseModel


def test_activity_creation_defaults_to_draft():
    activity = Activity.create(
        name="Reforestación San Pedro",
        owner_id="usr_123",
        image_url="https://res.cloudinary.com/test.webp",
        date=datetime.now(timezone.utc),
        capacity=15,
    )
    assert activity.status == ActivityStatus.DRAFT
    assert activity.capacity == 15
    assert activity.name == "Reforestación San Pedro"


def test_activity_capacity_must_be_positive_integer():
    with pytest.raises(ValueError, match="mayor a cero"):
        Activity.create(
            name="Actividad Cero",
            owner_id="usr_123",
            image_url="https://res.cloudinary.com/test.webp",
            date=datetime.now(timezone.utc),
            capacity=0,
        )

    with pytest.raises(ValueError, match="mayor a cero"):
        Activity.create(
            name="Actividad Negativa",
            owner_id="usr_123",
            image_url="https://res.cloudinary.com/test.webp",
            date=datetime.now(timezone.utc),
            capacity=-5,
        )


def test_base_model_soft_delete_and_restore():
    model = BaseModel()
    assert model.deleted_date is None

    model.soft_delete()
    assert model.deleted_date is not None

    model.restore()
    assert model.deleted_date is None
