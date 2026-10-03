"""
app/core/integrations/cloudinary.py

Integración con el servicio Cloudinary para subida y almacenamiento de imágenes
en la carpeta dedicada `sumate/activities`.
"""

import logging
from typing import BinaryIO
import cloudinary
import cloudinary.uploader

from app.core.config import settings

logger = logging.getLogger(__name__)

_is_configured = False


def configure_cloudinary() -> None:
    """Configura la instancia de Cloudinary con las credenciales del entorno."""
    global _is_configured
    if not _is_configured:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )
        _is_configured = True


def upload_activity_image(file: BinaryIO | bytes, filename: str | None = None) -> str:
    """
    Sube un archivo de imagen a Cloudinary en la carpeta `sumate/activities`.

    Retorna la URL segura (HTTPS) del recurso alojado.
    """
    configure_cloudinary()

    upload_options = {
        "folder": "sumate/activities",
        "resource_type": "image",
    }
    if filename:
        upload_options["public_id_prefix"] = filename

    logger.info("Subiendo imagen de actividad a Cloudinary (folder: sumate/activities)...")
    result = cloudinary.uploader.upload(file, **upload_options)
    secure_url = result.get("secure_url")

    if not secure_url:
        raise ValueError("Cloudinary no retornó una URL segura para la imagen.")

    logger.info("Imagen subida exitosamente: %s", secure_url)
    return secure_url
