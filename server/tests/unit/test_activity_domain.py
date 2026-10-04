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


def test_list_activities_query_handler_propagates_creator_image():
    from unittest.mock import MagicMock
    from app.modules.activities.application.queries.list_activities import (
        ListActivitiesQuery,
        ListActivitiesQueryHandler,
    )

    activity = Activity.create(
        name="Actividad Prueba",
        owner_id="usr_123",
        image_url="https://res.cloudinary.com/test.webp",
        date=datetime.now(timezone.utc),
        capacity=5,
        creator_name="Ana Pérez",
        creator_image="https://example.com/avatar.jpg",
    )

    repo = MagicMock()
    repo.list_activities.return_value = [activity]

    handler = ListActivitiesQueryHandler(repo)
    result = handler.execute(ListActivitiesQuery(scope="mine", current_user_id="usr_123"))

    assert len(result.items) == 1
    assert result.items[0].creator_name == "Ana Pérez"
    assert result.items[0].creator_image == "https://example.com/avatar.jpg"

