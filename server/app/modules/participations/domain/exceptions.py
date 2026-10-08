from app.shared.domain.exceptions import ConflictException, NotFoundException, ValidationException


class CannotJoinPastActivityException(ValidationException):
    code = "CANNOT_JOIN_PAST_ACTIVITY"
    message = "No es posible unirse a una actividad que ya ha concluido o cuya fecha ya transcurrió."


class CannotJoinOwnActivityException(ValidationException):
    code = "CANNOT_JOIN_OWN_ACTIVITY"
    message = "El organizador no puede inscribirse en su propia actividad."


class ActivityCapacityExceededException(ConflictException):
    code = "ACTIVITY_CAPACITY_EXCEEDED"
    message = "La actividad ha alcanzado su capacidad máxima de participantes."


class AlreadyParticipatingException(ConflictException):
    code = "ALREADY_PARTICIPATING"
    message = "El usuario ya se encuentra registrado en esta actividad."


class ParticipationNotFoundException(NotFoundException):
    code = "PARTICIPATION_NOT_FOUND"
    message = "No se encontró el registro de participación para esta actividad."


class CannotLeavePastActivityException(ValidationException):
    code = "CANNOT_LEAVE_PAST_ACTIVITY"
    message = "No es posible cancelar la participación de una actividad que ya ha concluido o cuya fecha ya transcurrió."
