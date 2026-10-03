"""
app/modules/events/domain/exceptions.py

Excepciones de negocio para el módulo de eventos.
"""

from app.shared.domain.exceptions import NotFoundException, ValidationException


class EventNotFoundException(NotFoundException):
    """El evento solicitado no existe o fue dado de baja."""
    code = "EVENT_NOT_FOUND"
    message = "El evento no fue encontrado."


class InvalidEventNameException(ValidationException):
    """El nombre del evento no cumple con los requisitos del dominio."""
    code = "INVALID_EVENT_NAME"
    message = "El nombre del evento no puede estar vacío."


class InvalidEventDateException(ValidationException):
    """La fecha del evento debe ser una fecha válida."""
    code = "INVALID_EVENT_DATE"
    message = "La fecha del evento es inválida."


class InvalidEventImageException(ValidationException):
    """La URL de la imagen del evento es requerida y debe ser válida."""
    code = "INVALID_EVENT_IMAGE"
    message = "La imagen del evento es obligatoria."
