"""Clases del dominio: entidades, clientes, servicios y reservas."""

from abc import ABC, abstractmethod
from excepciones import (
    DatosInvalidosError,
    ReservaInvalidaError,
    EstadoReservaError,
    ServicioNoDisponibleError,
)


class Entidad(ABC):
    """Clase abstracta general para las entidades del sistema."""

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise DatosInvalidosError("El identificador es obligatorio.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def obtener_resumen(self):
        """Devuelve una descripción breve de la entidad."""
        raise NotImplementedError


class Cliente(Entidad):
    """Representa a un cliente y protege sus datos mediante encapsulación."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)

        if not isinstance(nombre, str) or len(nombre.strip()) < 2:
            raise DatosInvalidosError("El nombre del cliente debe tener al menos 2 caracteres.")

        if not isinstance(correo, str) or correo.count("@") != 1:
            raise DatosInvalidosError("El correo electrónico no tiene un formato válido.")

        dominio = correo.split("@")[1]
        if "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
            raise DatosInvalidosError("El dominio del correo electrónico no es válido.")

        if not isinstance(telefono, str):
            raise DatosInvalidosError("El teléfono debe ingresarse como texto.")

        telefono_limpio = "".join(caracter for caracter in telefono if caracter.isdigit())
        if len(telefono_limpio) < 7:
            raise DatosInvalidosError("El teléfono debe contener al menos 7 dígitos.")

        self.__nombre = nombre.strip()
        self.__correo = correo.strip().lower()
        self.__telefono = telefono_limpio

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    @property
    def telefono(self):
        return self.__telefono

    def obtener_resumen(self):
        return (
            f"Cliente {self.identificador}: {self.__nombre} | "
            f"Correo: {self.__correo} | Teléfono: {self.__telefono}"
        )


class Servicio(Entidad, ABC):
    """Clase abstracta que define el comportamiento común de los servicios."""

    def __init__(self, identificador, nombre, tarifa_base, disponible=True):
        super().__init__(identificador)

        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio es obligatorio.")

        if (
            not isinstance(tarifa_base, (int, float))
            or isinstance(tarifa_base, bool)
            or tarifa_base <= 0
        ):
            raise DatosInvalidosError("La tarifa base debe ser un número mayor que cero.")

        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")

        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    def cambiar_disponibilidad(self, disponible):
        if not isinstance(disponible, bool):
            raise DatosInvalidosError("La disponibilidad debe ser verdadera o falsa.")
        self._disponible = disponible

    @abstractmethod
    def validar_parametros(self, duracion, impuesto=0.19, descuento=0.0):
        """Valida los parámetros comunes y los específicos del servicio."""
        if (
            not isinstance(duracion, (int, float))
            or isinstance(duracion, bool)
            or duracion <= 0
        ):
            raise DatosInvalidosError("La duración debe ser un número mayor que cero.")

        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if (
                not isinstance(valor, (int, float))
                or isinstance(valor, bool)
                or valor < 0
                or valor > 1
            ):
                raise DatosInvalidosError(
                    f"El {nombre} debe expresarse como un valor entre 0 y 1."
                )

    def _calcular_total(self, duracion, impuesto, descuento):
        """Aplica descuento e impuesto al subtotal del servicio."""
        subtotal = self._tarifa_base * duracion
        subtotal_con_descuento = subtotal * (1 - descuento)
        total = subtotal_con_descuento * (1 + impuesto)
        return round(total, 2)

    @abstractmethod
    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        """Calcula el costo; los parámetros opcionales permiten distintas variantes."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        """Describe el servicio especializado."""
        raise NotImplementedError

    def obtener_resumen(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return f"{self.identificador} - {self._nombre} | ${self._tarifa_base:.2f} | {estado}"


class ReservaSala(Servicio):
    """Servicio de reserva de salas, cobrado por hora."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)

        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala debe ser un entero positivo.")

        self.__capacidad = capacidad

    def validar_parametros(self, duracion, impuesto=0.19, descuento=0.0):
        super().validar_parametros(duracion, impuesto, descuento)
        if self.__capacidad <= 0:
            raise DatosInvalidosError("La capacidad de la sala no es válida.")

    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        self.validar_parametros(duracion, impuesto, descuento)
        return self._calcular_total(duracion, impuesto, descuento)

    def describir(self):
        return (
            f"Reserva de sala: {self.nombre}. "
            f"Capacidad máxima: {self.__capacidad} personas. "
            f"Tarifa por hora: ${self.tarifa_base:.2f}."
        )


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos, cobrado por día."""

    def __init__(self, identificador, nombre, tarifa_dia, tipo_equipo, disponible=True):
        super().__init__(identificador, nombre, tarifa_dia, disponible)

        if not isinstance(tipo_equipo, str) or not tipo_equipo.strip():
            raise DatosInvalidosError("Debe especificarse el tipo de equipo.")

        self.__tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, duracion, impuesto=0.19, descuento=0.0):
        super().validar_parametros(duracion, impuesto, descuento)
        if not self.__tipo_equipo:
            raise DatosInvalidosError("El tipo de equipo no puede estar vacío.")

    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        self.validar_parametros(duracion, impuesto, descuento)
        return self._calcular_total(duracion, impuesto, descuento)

    def describir(self):
        return (
            f"Alquiler de {self.__tipo_equipo}: {self.nombre}. "
            f"Tarifa por día: ${self.tarifa_base:.2f}."
        )


class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría especializada, cobrado por hora."""

    def __init__(self, identificador, nombre, tarifa_hora, especialidad, disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)

        if not isinstance(especialidad, str) or not especialidad.strip():
            raise DatosInvalidosError("Debe especificarse la especialidad de la asesoría.")

        self.__especialidad = especialidad.strip()

    def validar_parametros(self, duracion, impuesto=0.19, descuento=0.0):
        super().validar_parametros(duracion, impuesto, descuento)
        if not self.__especialidad:
            raise DatosInvalidosError("La especialidad no puede estar vacía.")

    def calcular_costo(self, duracion=1, impuesto=0.19, descuento=0.0):
        self.validar_parametros(duracion, impuesto, descuento)
        return self._calcular_total(duracion, impuesto, descuento)

    def describir(self):
        return (
            f"Asesoría en {self.__especialidad}: {self.nombre}. "
            f"Tarifa por hora: ${self.tarifa_base:.2f}."
        )


class Reserva(Entidad):
    """Integra un cliente, un servicio, la duración y el estado de la reserva."""

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        duracion,
        impuesto=0.19,
        descuento=0.0,
    ):
        super().__init__(identificador)

        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva debe estar asociada a un cliente válido.")

        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva debe estar asociada a un servicio válido.")

        servicio.validar_parametros(duracion, impuesto, descuento)

        self.__cliente = cliente
        self.__servicio = servicio
        self.__duracion = duracion
        self.__impuesto = impuesto
        self.__descuento = descuento
        self.__estado = "PENDIENTE"
        self.__total = None

    @property
    def estado(self):
        return self.__estado

    @property
    def total(self):
        return self.__total

    def procesar(self):
        """Procesa el cálculo y encadena el error original si ocurre un fallo."""
        try:
            return self.__servicio.calcular_costo(
                self.__duracion, self.__impuesto, self.__descuento
            )
        except Exception as error:
            raise ReservaInvalidaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

    def confirmar(self):
        if self.__estado != "PENDIENTE":
            raise EstadoReservaError(
                f"No se puede confirmar una reserva en estado {self.__estado}."
            )

        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError(
                f"El servicio {self.__servicio.identificador} no está disponible."
            )

        total_calculado = self.procesar()
        self.__servicio.cambiar_disponibilidad(False)
        self.__total = total_calculado
        self.__estado = "CONFIRMADA"
        return self.__total

    def cancelar(self):
        if self.__estado not in ("PENDIENTE", "CONFIRMADA"):
            raise EstadoReservaError(
                f"No se puede cancelar una reserva en estado {self.__estado}."
            )

        if self.__estado == "CONFIRMADA":
            self.__servicio.cambiar_disponibilidad(True)

        self.__estado = "CANCELADA"
        return f"Reserva {self.identificador} cancelada correctamente."

    def obtener_resumen(self):
        total = "Pendiente de cálculo" if self.__total is None else f"${self.__total:.2f}"
        return (
            f"Reserva {self.identificador} | Cliente: {self.__cliente.nombre} | "
            f"Servicio: {self.__servicio.nombre} | Duración: {self.__duracion} | "
            f"Estado: {self.__estado} | Total: {total}"
        )
