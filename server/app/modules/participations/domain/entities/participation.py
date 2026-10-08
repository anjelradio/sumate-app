from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass
class Participation:
    id: UUID
    activity_id: UUID
    user_id: str

    @classmethod
    def create(
        cls,
        activity_id: UUID,
        user_id: str,
    ) -> "Participation":
        return cls(
            id=uuid4(),
            activity_id=activity_id,
            user_id=user_id,
        )
