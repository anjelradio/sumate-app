import logging
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import UUID

from app.core.dependencies import CurrentUser, DBSession, UoWDep
from app.core.errors.exceptions import APIHTTPException
from app.core.integrations.cloudinary import upload_activity_image
from app.modules.activities.application.queries.get_activity_detail import (
    GetActivityDetailQuery,
    GetActivityDetailQueryHandler,
)
from app.modules.activities.application.queries.list_activities import (
    ListActivitiesQuery,
    ListActivitiesQueryHandler,
)
from app.modules.activities.application.use_cases.close_activity import (
    CloseActivityCommand,
    CloseActivityUseCase,
)
from app.modules.activities.application.use_cases.create_activity import (
    CreateActivityCommand,
    CreateActivityUseCase,
)
from app.modules.activities.application.use_cases.publish_activity import (
    PublishActivityCommand,
    PublishActivityUseCase,
)
from app.modules.activities.application.use_cases.update_activity_description import (
    UpdateActivityDescriptionCommand,
    UpdateActivityDescriptionUseCase,
)
from app.modules.activities.application.use_cases.update_activity_image import (
    UpdateActivityImageCommand,
    UpdateActivityImageUseCase,
)
from app.modules.activities.application.use_cases.update_activity_info import (
    UpdateActivityInfoCommand,
    UpdateActivityInfoUseCase,
)
from app.modules.activities.application.use_cases.update_activity_location import (
    UpdateActivityLocationCommand,
    UpdateActivityLocationUseCase,
)
from app.modules.activities.domain.exceptions import ActivityNotFoundException
from app.modules.activities.infrastructure.api.schemas.activity_schemas import (
    ActivityDetailDataRead,
    ActivityDetailRead,
    ActivityListItemRead,
    ActivityListRead,
    UpdateActivityInfoRequest,
    UpdateDescriptionRequest,
    UpdateLocationRequest,
)
from app.modules.activities.infrastructure.persistence.repositories.sqlmodel_activity_repository import (
    SQLModelActivityRepository,
)
from fastapi import APIRouter, File, Form, Query, Response, UploadFile, status

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
                creator_image=item.creator_image,
            )
            for item in dto.items
        ]
    )


@router.get(
    "/{activity_id}",
    response_model=ActivityDetailRead,
    summary="Obtener detalle de una actividad",
    description="Retorna el detalle completo de la actividad. Si es borrador, solo el creador tiene acceso.",
)
def get_activity_detail(
    activity_id: UUID,
    current_user: CurrentUser,
    db: DBSession,
) -> ActivityDetailRead:
    repository = SQLModelActivityRepository(db)
    handler = GetActivityDetailQueryHandler(repository)
    try:
        dto = handler.execute(
            GetActivityDetailQuery(
                activity_id=activity_id,
                current_user_id=current_user.user_id,
            )
        )
    except ActivityNotFoundException:
        raise APIHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            code="ACTIVITY_NOT_FOUND",
            message="La actividad no fue encontrada o no está disponible.",
        )

    detail_data = (
        ActivityDetailDataRead(
            id=dto.detail.id,
            activity_id=dto.detail.activity_id,
            latitude=dto.detail.latitude,
            longitude=dto.detail.longitude,
            place=dto.detail.place,
            address=dto.detail.address,
            description=dto.detail.description,
        )
        if dto.detail
        else None
    )

    return ActivityDetailRead(
        id=dto.id,
        name=dto.name,
        owner_id=dto.owner_id,
        creator_name=dto.creator_name,
        creator_image=dto.creator_image,
        image_url=dto.image_url,
        date=dto.date,
        capacity=dto.capacity,
        status=dto.status,
        is_owner=(dto.owner_id == current_user.user_id),
        detail=detail_data,
    )


@router.patch(
    "/{activity_id}/location",
    status_code=status.HTTP_200_OK,
    summary="Actualizar ubicación de la actividad",
)
async def update_activity_location(
    activity_id: UUID,
    payload: UpdateLocationRequest,
    current_user: CurrentUser,
    uow: UoWDep,
) -> Response:
    repository = SQLModelActivityRepository(uow.session)
    use_case = UpdateActivityLocationUseCase(repository, uow)
    await use_case.execute(
        UpdateActivityLocationCommand(
            activity_id=activity_id,
            owner_id=current_user.user_id,
            latitude=payload.latitude,
            longitude=payload.longitude,
            place=payload.place,
        )
    )
    return Response(status_code=status.HTTP_200_OK)


@router.patch(
    "/{activity_id}/description",
    status_code=status.HTTP_200_OK,
    summary="Actualizar descripción de la actividad",
)
def update_activity_description(
    activity_id: UUID,
    payload: UpdateDescriptionRequest,
    current_user: CurrentUser,
    uow: UoWDep,
) -> Response:
    repository = SQLModelActivityRepository(uow.session)
    use_case = UpdateActivityDescriptionUseCase(repository, uow)
    use_case.execute(
        UpdateActivityDescriptionCommand(
            activity_id=activity_id,
            owner_id=current_user.user_id,
            description=payload.description,
        )
    )
    return Response(status_code=status.HTTP_200_OK)


@router.patch(
    "/{activity_id}/image",
    status_code=status.HTTP_200_OK,
    summary="Reemplazar imagen de portada de la actividad",
)
async def update_activity_image(
    activity_id: UUID,
    current_user: CurrentUser,
    uow: UoWDep,
    image: Annotated[UploadFile, File(description="Nueva imagen de portada")],
) -> Response:
    image_content = await image.read()
    if not image_content:
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="EMPTY_IMAGE_FILE",
            message="El archivo de imagen no puede estar vacío.",
        )
    if len(image_content) > 2 * 1024 * 1024:
        raise APIHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="IMAGE_TOO_LARGE",
            message="La imagen no debe superar los 2MB.",
        )

    try:
        image_url = upload_activity_image(image_content, filename=image.filename)
    except Exception as exc:
        logger.error("Error al procesar la imagen con Cloudinary: %s", exc)
        raise APIHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            code="IMAGE_UPLOAD_FAILED",
            message=f"No se pudo cargar la imagen a Cloudinary: {exc}",
        )

    repository = SQLModelActivityRepository(uow.session)
    use_case = UpdateActivityImageUseCase(repository, uow)
    use_case.execute(
        UpdateActivityImageCommand(
            activity_id=activity_id,
            owner_id=current_user.user_id,
            image_url=image_url,
        )
    )
    return Response(status_code=status.HTTP_200_OK)


@router.patch(
    "/{activity_id}/info",
    status_code=status.HTTP_200_OK,
    summary="Actualizar datos base (título, fecha, cupos)",
)
def update_activity_info(
    activity_id: UUID,
    payload: UpdateActivityInfoRequest,
    current_user: CurrentUser,
    uow: UoWDep,
) -> Response:
    repository = SQLModelActivityRepository(uow.session)
    use_case = UpdateActivityInfoUseCase(repository, uow)
    use_case.execute(
        UpdateActivityInfoCommand(
            activity_id=activity_id,
            owner_id=current_user.user_id,
            name=payload.name,
            date=payload.date,
            capacity=payload.capacity,
        )
    )
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/{activity_id}/publish",
    status_code=status.HTTP_200_OK,
    summary="Publicar actividad",
)
def publish_activity(
    activity_id: UUID,
    current_user: CurrentUser,
    uow: UoWDep,
) -> Response:
    repository = SQLModelActivityRepository(uow.session)
    use_case = PublishActivityUseCase(repository, uow)
    use_case.execute(
        PublishActivityCommand(
            activity_id=activity_id,
            owner_id=current_user.user_id,
        )
    )
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    "/{activity_id}/close",
    status_code=status.HTTP_200_OK,
    summary="Cerrar convocatoria de la actividad",
)
def close_activity(
    activity_id: UUID,
    current_user: CurrentUser,
    uow: UoWDep,
) -> Response:
    repository = SQLModelActivityRepository(uow.session)
    use_case = CloseActivityUseCase(repository, uow)
    use_case.execute(
        CloseActivityCommand(
            activity_id=activity_id,
            owner_id=current_user.user_id,
        )
    )
    return Response(status_code=status.HTTP_200_OK)


