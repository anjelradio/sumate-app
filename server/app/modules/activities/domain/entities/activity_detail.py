from uuid import UUID, uuid4


class ActivityDetail:
    def __init__(
        self,
        id: UUID,
        activity_id: UUID,
        latitude: float | None = None,
        longitude: float | None = None,
        place: str | None = None,
        address: str | None = None,
        description: str | None = None,
    ) -> None:
        self.id = id
        self.activity_id = activity_id
        self.latitude, self.longitude = self.validate_coordinates(latitude, longitude)
        self.place = self.validate_place(place)
        self.address = self.validate_address(address)
        self.description = self.validate_description(description)

    @classmethod
    def create(
        cls,
        *,
        activity_id: UUID,
        latitude: float | None = None,
        longitude: float | None = None,
        place: str | None = None,
        address: str | None = None,
        description: str | None = None,
    ) -> "ActivityDetail":
        return cls(
            id=uuid4(),
            activity_id=activity_id,
            latitude=latitude,
            longitude=longitude,
            place=place,
            address=address,
            description=description,
        )

    def update_location(
        self,
        *,
        latitude: float | None,
        longitude: float | None,
        place: str | None = None,
        address: str | None = None,
    ) -> None:
        self.latitude, self.longitude = self.validate_coordinates(latitude, longitude)
        if place is not None:
            self.place = self.validate_place(place)
        if address is not None:
            self.address = self.validate_address(address)

    def update_description(self, description: str | None) -> None:
        self.description = self.validate_description(description)

    @staticmethod
    def validate_coordinates(
        latitude: float | None,
        longitude: float | None,
    ) -> tuple[float | None, float | None]:
        if latitude is None and longitude is None:
            return None, None
        if latitude is None or longitude is None:
            raise ValueError("Tanto la latitud como la longitud deben proporcionarse conjuntamente.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("La latitud debe estar comprendida entre -90.0 y 90.0 grados.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("La longitud debe estar comprendida entre -180.0 y 180.0 grados.")
        return float(latitude), float(longitude)

    @staticmethod
    def validate_place(place: str | None) -> str | None:
        if place is None:
            return None
        cleaned = place.strip()
        if len(cleaned) > 255:
            raise ValueError("El nombre del lugar no puede superar los 255 caracteres.")
        return cleaned or None

    @staticmethod
    def validate_address(address: str | None) -> str | None:
        if address is None:
            return None
        cleaned = address.strip()
        if len(cleaned) > 500:
            raise ValueError("La dirección no puede superar los 500 caracteres.")
        return cleaned or None

    @staticmethod
    def validate_description(description: str | None) -> str | None:
        if description is None:
            return None
        cleaned = description.strip()
        if len(cleaned) > 5000:
            raise ValueError("La descripción no puede superar los 5,000 caracteres.")
        return cleaned or None
