"""Lógica de gestión y registro de eventos del sistema Software FJ."""

import logging
from pathlib import Path

from excepciones import (
    DatosInvalidosError,
    ClienteDuplicadoError,
    ServicioDuplicadoError,
    ReservaInvalidaError,
)
from modelos import Cliente, Servicio, Reserva


class SistemaSoftwareFJ:
    """Administra clientes, servicios y reservas mediante listas en memoria."""

    def __init__(self):
        # Se utilizan listas internas, como solicita el ejercicio.
        self.__clientes = []
        self.__servicios = []
        self.__reservas = []
        self.__logger = self.__configurar_logger()

    def __configurar_logger(self):
        carpeta_logs = Path(__file__).resolve().parent / "logs"
        carpeta_logs.mkdir(parents=True, exist_ok=True)
        ruta_log = carpeta_logs / "software_fj.log"

        logger = logging.getLogger("SoftwareFJ")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        ruta_absoluta = str(ruta_log.resolve())
        existe_handler = any(
            getattr(handler, "baseFilename", None) == ruta_absoluta
            for handler in logger.handlers
        )

        if not existe_handler:
            manejador = logging.FileHandler(ruta_log, encoding="utf-8")
            formato = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            manejador.setFormatter(formato)
            logger.addHandler(manejador)

        return logger

    @staticmethod
    def __buscar_por_id(lista, identificador):
        """Busca una entidad dentro de una lista usando su identificador."""
        for elemento in lista:
            if elemento.identificador == identificador:
                return elemento
        raise KeyError(identificador)

    def registrar_error(self, contexto, error):
        """Registra errores capturados fuera de los métodos del sistema."""
        self.__logger.error(
            "%s: %s",
            contexto,
            error,
            exc_info=(type(error), error, error.__traceback__),
        )

    def registrar_cliente(self, cliente):
        try:
            if not isinstance(cliente, Cliente):
                raise DatosInvalidosError("El objeto que se intenta registrar no es un cliente.")

            if any(item.identificador == cliente.identificador for item in self.__clientes):
                raise ClienteDuplicadoError(
                    f"Ya existe el cliente {cliente.identificador}."
                )

            self.__clientes.append(cliente)

        except Exception:
            self.__logger.exception("Error al registrar un cliente.")
            raise
        else:
            self.__logger.info("Cliente registrado: %s", cliente.identificador)
            return cliente.obtener_resumen()

    def registrar_servicio(self, servicio):
        try:
            if not isinstance(servicio, Servicio):
                raise DatosInvalidosError("El objeto que se intenta registrar no es un servicio.")

            if any(item.identificador == servicio.identificador for item in self.__servicios):
                raise ServicioDuplicadoError(
                    f"Ya existe el servicio {servicio.identificador}."
                )

            self.__servicios.append(servicio)

        except Exception:
            self.__logger.exception("Error al registrar un servicio.")
            raise
        else:
            self.__logger.info("Servicio registrado: %s", servicio.identificador)
            return servicio.obtener_resumen()

    def crear_reserva(
        self, cliente_id, servicio_id, duracion, impuesto=0.19, descuento=0.0
    ):
        try:
            cliente = self.__buscar_por_id(self.__clientes, cliente_id)
            servicio = self.__buscar_por_id(self.__servicios, servicio_id)
            identificador = f"R{len(self.__reservas) + 1:03d}"

            reserva = Reserva(
                identificador,
                cliente,
                servicio,
                duracion,
                impuesto,
                descuento,
            )

        except KeyError as error:
            self.__logger.exception("No se encontró el cliente o servicio solicitado.")
            raise DatosInvalidosError(
                "No existe el cliente o el servicio indicado para crear la reserva."
            ) from error
        except Exception:
            self.__logger.exception("Error al crear una reserva.")
            raise
        else:
            self.__reservas.append(reserva)
            self.__logger.info("Reserva creada: %s", identificador)
            return reserva

    def confirmar_reserva(self, reserva_id):
        try:
            reserva = self.__buscar_por_id(self.__reservas, reserva_id)
        except KeyError as error:
            self.__logger.exception("Se intentó confirmar una reserva inexistente.")
            raise ReservaInvalidaError(
                f"No existe la reserva {reserva_id}."
            ) from error

        try:
            total = reserva.confirmar()
        except Exception:
            self.__logger.exception("Error al confirmar la reserva %s.", reserva_id)
            raise
        else:
            self.__logger.info(
                "Reserva confirmada: %s | Total: $%.2f", reserva_id, total
            )
            return total
        finally:
            self.__logger.info("Finalizó el intento de confirmación de %s.", reserva_id)

    def cancelar_reserva(self, reserva_id):
        try:
            reserva = self.__buscar_por_id(self.__reservas, reserva_id)
        except KeyError as error:
            self.__logger.exception("Se intentó cancelar una reserva inexistente.")
            raise ReservaInvalidaError(
                f"No existe la reserva {reserva_id}."
            ) from error

        try:
            resultado = reserva.cancelar()
        except Exception:
            self.__logger.exception("Error al cancelar la reserva %s.", reserva_id)
            raise
        else:
            self.__logger.info("Reserva cancelada: %s", reserva_id)
            return resultado
        finally:
            self.__logger.info("Finalizó el intento de cancelación de %s.", reserva_id)

    def listar_clientes(self):
        return [cliente.obtener_resumen() for cliente in self.__clientes]

    def listar_servicios(self):
        return [servicio.obtener_resumen() for servicio in self.__servicios]

    def listar_reservas(self):
        return [reserva.obtener_resumen() for reserva in self.__reservas]
