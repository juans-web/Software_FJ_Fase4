"""Punto de entrada: ejecuta una simulación de operaciones del sistema Software FJ."""

from excepciones import DatosInvalidosError
from modelos import (
    Cliente,
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada,
)
from sistema import SistemaSoftwareFJ


def ejecutar_operacion(sistema, numero, descripcion, operacion):
    """Ejecuta una prueba aislada para que un error no detenga las demás."""
    print(f"\n{numero}. {descripcion}")
    try:
        resultado = operacion()
    except Exception as error:
        sistema.registrar_error(descripcion, error)
        print(f"Resultado: error controlado -> {error}")
    else:
        if resultado is not None:
            print(f"Resultado: {resultado}")
        else:
            print("Resultado: operación realizada correctamente.")
    finally:
        print("Fin de la operación.")


def main():
    sistema = SistemaSoftwareFJ()

    print("=" * 65)
    print("SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("Simulación de clientes, servicios, reservas y excepciones")
    print("=" * 65)

    # 1. Registro válido de un cliente.
    ejecutar_operacion(
        sistema, 1, "Registrar cliente válido C001",
        lambda: sistema.registrar_cliente(
            Cliente("C001", "Laura Gómez", "laura@gmail.com", "3001234567")
        ),
    )

    # 2. Registro válido de un segundo cliente.
    ejecutar_operacion(
        sistema, 2, "Registrar cliente válido C002",
        lambda: sistema.registrar_cliente(
            Cliente("C002", "Carlos Pérez", "carlos@gmail.com", "3107654321")
        ),
    )

    # 3. Registro inválido: correo sin formato correcto.
    ejecutar_operacion(
        sistema, 3, "Intentar registrar cliente con correo inválido",
        lambda: sistema.registrar_cliente(
            Cliente("C003", "Ana Ruiz", "ana-correo-invalido", "3001112233")
        ),
    )

    # 4. Registro duplicado.
    ejecutar_operacion(
        sistema, 4, "Intentar registrar nuevamente el cliente C001",
        lambda: sistema.registrar_cliente(
            Cliente("C001", "Laura Gómez", "laura@gmail.com", "3001234567")
        ),
    )

    # 5. Creación correcta de un servicio de reserva de sala.
    ejecutar_operacion(
        sistema, 5, "Registrar servicio de reserva de sala S001",
        lambda: sistema.registrar_servicio(
            ReservaSala("S001", "Sala Ejecutiva", 50000, 20)
        ),
    )

    # 6. Creación correcta de un servicio de alquiler de equipos.
    ejecutar_operacion(
        sistema, 6, "Registrar servicio de alquiler de equipo S002",
        lambda: sistema.registrar_servicio(
            AlquilerEquipo("S002", "Alquiler de proyector", 35000, "Proyector HD")
        ),
    )

    # 7. Creación correcta de un servicio de asesoría.
    ejecutar_operacion(
        sistema, 7, "Registrar servicio de asesoría especializada S003",
        lambda: sistema.registrar_servicio(
            AsesoriaEspecializada(
                "S003", "Asesoría tecnológica", 80000, "Desarrollo de software"
            )
        ),
    )

    # 8. Creación incorrecta: tarifa negativa.
    ejecutar_operacion(
        sistema, 8, "Intentar crear un servicio con tarifa negativa",
        lambda: sistema.registrar_servicio(
            ReservaSala("S004", "Sala inválida", -10000, 10)
        ),
    )

    # 9. Crear una reserva válida.
    ejecutar_operacion(
        sistema, 9, "Crear reserva R001 para el cliente C001 y la sala S001",
        lambda: sistema.crear_reserva("C001", "S001", 2).obtener_resumen(),
    )

    # 10. Confirmar la reserva R001.
    ejecutar_operacion(
        sistema, 10, "Confirmar la reserva R001",
        lambda: f"Costo total: ${sistema.confirmar_reserva('R001'):.2f}",
    )

    # 11. Crear una segunda reserva para el mismo servicio.
    ejecutar_operacion(
        sistema, 11, "Crear reserva R002 para el mismo servicio S001",
        lambda: sistema.crear_reserva("C002", "S001", 1).obtener_resumen(),
    )

    # 12. Fallo controlado: el servicio ya está ocupado.
    ejecutar_operacion(
        sistema, 12, "Intentar confirmar R002 mientras S001 no está disponible",
        lambda: sistema.confirmar_reserva("R002"),
    )

    # 13. Crear una reserva de asesoría con descuento.
    ejecutar_operacion(
        sistema, 13, "Crear reserva R003 de asesoría con descuento del 10%",
        lambda: sistema.crear_reserva(
            "C002", "S003", 2, impuesto=0.19, descuento=0.10
        ).obtener_resumen(),
    )

    # 14. Confirmar la reserva R003.
    ejecutar_operacion(
        sistema, 14, "Confirmar la reserva R003",
        lambda: f"Costo total: ${sistema.confirmar_reserva('R003'):.2f}",
    )

    # 15. Cancelar una reserva confirmada.
    ejecutar_operacion(
        sistema, 15, "Cancelar la reserva R003",
        lambda: sistema.cancelar_reserva("R003"),
    )

    # 16. Intentar confirmar una reserva inexistente.
    ejecutar_operacion(
        sistema, 16, "Intentar confirmar una reserva inexistente",
        lambda: sistema.confirmar_reserva("R999"),
    )

    print("\n" + "=" * 65)
    print("RESUMEN FINAL")
    print("=" * 65)

    print("\nCLIENTES:")
    for elemento in sistema.listar_clientes():
        print("-", elemento)

    print("\nSERVICIOS:")
    for elemento in sistema.listar_servicios():
        print("-", elemento)

    print("\nRESERVAS:")
    for elemento in sistema.listar_reservas():
        print("-", elemento)

    print("\nLos eventos y errores se registraron en: logs/software_fj.log")
    print("La simulación terminó sin detenerse por los errores controlados.")


if __name__ == "__main__":
    main()
