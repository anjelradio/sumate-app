"""
app/modules/events/infrastructure/api/routers/event_router.py

Router de FastAPI para el módulo de eventos.
Prefijo canónico /events. En app/main.py se incluye con prefix="/api".
"""

from datetime import datetime, timezone
import logging
from typing import Annotated, Literal

from fastapi import APIRouter, File, Form, Query, Response, UploadFile, status

from app.core.dependencies import CurrentUser, DBSession, UoWDep
from app.core.errors.exceptions import APIHTTPException
from app.core.integrations.cloudinary import upload_event_image
from app.modules.events.application.queries.list_events import (
    ListEventsQuery,
    ListEventsQueryHandler,
)
from app.modules.events.application.use_cases.create_event import (
    CreateEventCommand,
    CreateEventUseCase,
)
from app.modules.events.infrastructure.api.schemas.event_schemas import (
    EventListItemRead,
    EventListRead,
)
from app.modules.events.infrastructure.persistence.repositories.sqlmodel_event_repository import (
    SQLModelEventRepository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Eventos"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo evento",
    description="Sube la imagen a Cloudinary (carpeta sumate/events) y registra el evento.",
)
async def create_event(
    current_user: CurrentUser,
    uow: UoWDep,
    name: Annotated[str, Form(description="Nombre del evento")],
    date: Annotated[str, Form(description="Fecha y hora de realización del evento")],
    image: Annotated[UploadFile, File(description="Imagen del evento")],
) -> Response:
    if not name or not name.strip():
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_EVENT_NAME",
            message="El nombre del evento es requerido.",
        )

    try:
        clean_date_str = date.strip().replace("Z", "+00:00")
        parsed_date = datetime.fromisoformat(clean_date_str)
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
    except ValueError:
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_EVENT_DATE",
            message="El formato de la fecha es inválido. Use ISO 8601 o YYYY-MM-DDTHH:MM.",
        )

    try:
        # Subir imagen a Cloudinary
        image_content = await image.read()
        if not image_content:
            raise APIHTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                code="EMPTY_IMAGE_FILE",
                message="El archivo de imagen no puede estar vacío.",
            )

        image_url = upload_event_image(image_content, filename=image.filename)
    except Exception as exc:
        logger.error("Error al procesar la imagen con Cloudinary: %s", exc)
        raise APIHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="IMAGE_UPLOAD_FAILED",
            message=f"No se pudo cargar la imagen a Cloudinary: {exc}",
        )

    # Persistir evento
    repository = SQLModelEventRepository(uow.session)
    use_case = CreateEventUseCase(repository, uow)

    use_case.execute(
        CreateEventCommand(
            name=name.strip(),
            owner_id=current_user.user_id,
            image_url=image_url,
            date=parsed_date,
        )
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.get(
    "",
    response_model=EventListRead,
    summary="Listar eventos",
    description="Retorna la lista de eventos activos según el scope indicado ('mine' por defecto o 'others').",
)
def list_events(
    current_user: CurrentUser,
    db: DBSession,
    scope: Annotated[
        Literal["mine", "others"],
        Query(description="Ámbito de búsqueda: 'mine' para eventos propios, 'others' para terceros"),
    ] = "mine",
) -> EventListRead:
    repository = SQLModelEventRepository(db)
    handler = ListEventsQueryHandler(repository)
    dto = handler.execute(
        ListEventsQuery(
            scope=scope,
            current_user_id=current_user.user_id,
        )
    )

    return EventListRead(
        items=[
            EventListItemRead(
                id=item.id,
                name=item.name,
                image_url=item.image_url,
                date=item.date,
                owner_id=item.owner_id,
                creator_name=item.creator_name,
            )
            for item in dto.items
        ]
    )
