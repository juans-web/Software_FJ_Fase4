"""Excepciones personalizadas del sistema Software FJ."""

class ErrorSoftwareFJ(Exception):
    """Clase base para los errores controlados de la aplicación."""


class DatosInvalidosError(ErrorSoftwareFJ):
    """Se genera cuando un dato no cumple las validaciones."""


class ClienteDuplicadoError(ErrorSoftwareFJ):
    """Se genera cuando se intenta registrar un cliente existente."""


class ServicioDuplicadoError(ErrorSoftwareFJ):
    """Se genera cuando se intenta registrar un servicio existente."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se genera cuando se intenta reservar un servicio no disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se genera cuando una reserva no puede crearse o procesarse."""


class EstadoReservaError(ErrorSoftwareFJ):
    """Se genera cuando una operación no corresponde al estado de la reserva."""
