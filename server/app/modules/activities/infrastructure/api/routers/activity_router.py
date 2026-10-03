"""
app/modules/activities/infrastructure/api/routers/activity_router.py

Router de FastAPI para el módulo de actividades.
Prefijo canónico /activities. En app/main.py se incluye con prefix="/api".
"""

from datetime import datetime, timezone
import logging
from typing import Annotated, Literal

from fastapi import APIRouter, File, Form, Query, Response, UploadFile, status

from app.core.dependencies import CurrentUser, DBSession, UoWDep
from app.core.errors.exceptions import APIHTTPException
from app.core.integrations.cloudinary import upload_activity_image
from app.modules.activities.application.queries.list_activities import (
    ListActivitiesQuery,
    ListActivitiesQueryHandler,
)
from app.modules.activities.application.use_cases.create_activity import (
    CreateActivityCommand,
    CreateActivityUseCase,
)
from app.modules.activities.infrastructure.api.schemas.activity_schemas import (
    ActivityListItemRead,
    ActivityListRead,
)
from app.modules.activities.infrastructure.persistence.repositories.sqlmodel_activity_repository import (
    SQLModelActivityRepository,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/activities", tags=["Actividades"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva actividad",
    description="Sube la imagen a Cloudinary (carpeta sumate/activities) y registra la actividad.",
)
async def create_activity(
    current_user: CurrentUser,
    uow: UoWDep,
    name: Annotated[str, Form(description="Nombre de la actividad")],
    date: Annotated[str, Form(description="Fecha y hora de realización de la actividad")],
    capacity: Annotated[int, Form(description="Cantidad de cupos o plazas", ge=1, le=10000)] = 1,
    image: Annotated[UploadFile, File(description="Imagen de la actividad")] = ...,
) -> Response:
    if not name or not name.strip():
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_ACTIVITY_NAME",
            message="El nombre de la actividad es requerido.",
        )

    if capacity <= 0 or capacity > 10000:
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_CAPACITY",
            message="La cantidad de plazas debe ser mayor a cero y no superar 10,000.",
        )

    try:
        clean_date_str = date.strip().replace("Z", "+00:00")
        parsed_date = datetime.fromisoformat(clean_date_str)
        if parsed_date.tzinfo is None:
            parsed_date = parsed_date.replace(tzinfo=timezone.utc)
    except ValueError:
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="INVALID_ACTIVITY_DATE",
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

        image_url = upload_activity_image(image_content, filename=image.filename)
    except Exception as exc:
        logger.error("Error al procesar la imagen con Cloudinary: %s", exc)
        raise APIHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="IMAGE_UPLOAD_FAILED",
            message=f"No se pudo cargar la imagen a Cloudinary: {exc}",
        )

    # Persistir actividad
    repository = SQLModelActivityRepository(uow.session)
    use_case = CreateActivityUseCase(repository, uow)

    use_case.execute(
        CreateActivityCommand(
            name=name.strip(),
            owner_id=current_user.user_id,
            image_url=image_url,
            date=parsed_date,
            capacity=capacity,
        )
    )

    return Response(status_code=status.HTTP_201_CREATED)


@router.get(
    "",
    response_model=ActivityListRead,
    summary="Listar actividades",
    description="Retorna la lista de actividades activas según el scope indicado ('mine' por defecto o 'others').",
)
def list_activities(
    current_user: CurrentUser,
    db: DBSession,
    scope: Annotated[
        Literal["mine", "others"],
        Query(description="Ámbito de búsqueda: 'mine' para actividades propias, 'others' para terceros"),
    ] = "mine",
) -> ActivityListRead:
    repository = SQLModelActivityRepository(db)
    handler = ListActivitiesQueryHandler(repository)
    dto = handler.execute(
        ListActivitiesQuery(
            scope=scope,
            current_user_id=current_user.user_id,
        )
    )

    return ActivityListRead(
        items=[
            ActivityListItemRead(
                id=item.id,
                name=item.name,
                image_url=item.image_url,
                date=item.date,
                owner_id=item.owner_id,
                capacity=item.capacity,
                status=item.status,
                creator_name=item.creator_name,
            )
            for item in dto.items
        ]
    )
