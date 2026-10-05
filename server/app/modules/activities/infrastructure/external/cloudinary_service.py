import logging

from app.core.integrations.cloudinary import upload_activity_image
from app.modules.activities.domain.exceptions import InvalidActivityImageException
from fastapi import UploadFile

logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE_BYTES = 2 * 1024 * 1024


class CloudinaryService:
    @staticmethod
    async def upload_activity_cover(image: UploadFile) -> str:
        content = await image.read()
        if not content:
            raise InvalidActivityImageException("El archivo de imagen no puede estar vacío.")

        if len(content) > MAX_IMAGE_SIZE_BYTES:
            raise InvalidActivityImageException("La imagen no debe superar los 2MB.")

        try:
            return upload_activity_image(content, filename=image.filename)
        except Exception as exc:
            logger.error("Error al procesar la imagen con Cloudinary: %s", exc)
            raise InvalidActivityImageException(f"No se pudo cargar la imagen a Cloudinary: {exc}")
