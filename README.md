# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto académico del curso Programación (213023), UNAD - Fase 4.

## 1. Objetivo

Desarrollar una aplicación en Python orientada a objetos para gestionar clientes, servicios y reservas de la empresa ficticia Software FJ. El programa utiliza objetos y estructuras de datos en memoria, sin motores de bases de datos.

## 2. Requisitos

- Python 3 instalado.
- No requiere instalar librerías externas.

## 3. Estructura

```text
Software_FJ/
├── main.py
├── modelos.py
├── excepciones.py
├── sistema.py
├── README.md
└── logs/
    └── .gitkeep
```

## 4. Ejecución

1. Descomprimir la carpeta.
2. Abrir la carpeta `Software_FJ` en Visual Studio Code o en una terminal.
3. Ejecutar:

```bash
python main.py
```

En algunos equipos Windows también puede ser necesario:

```bash
py main.py
```

El programa ejecuta una simulación de operaciones válidas e inválidas. Los errores se controlan para que la ejecución continúe y se registran en `logs/software_fj.log`.

## 5. Clases implementadas

- `Entidad`: clase abstracta general.
- `Cliente`: representa a los clientes y encapsula sus datos personales.
- `Servicio`: clase abstracta de la que heredan los servicios especializados.
- `ReservaSala`: servicio de reserva de salas, con cobro por hora.
- `AlquilerEquipo`: servicio de alquiler de equipos, con cobro por día.
- `AsesoriaEspecializada`: servicio de asesoría, con cobro por hora.
- `Reserva`: integra cliente, servicio, duración, estado y costo.
- `SistemaSoftwareFJ`: administra los registros y las operaciones.

## 6. Principios de programación orientada a objetos

- **Abstracción:** se implementa mediante las clases abstractas `Entidad` y `Servicio`.
- **Herencia:** `Cliente`, `Servicio` y `Reserva` heredan de `Entidad`; los tres servicios especializados heredan de `Servicio`.
- **Encapsulación:** los datos personales del cliente se almacenan en atributos privados.
- **Polimorfismo:** cada servicio especializado implementa sus propias versiones de `calcular_costo`, `describir` y `validar_parametros`.
- **Métodos con parámetros opcionales:** `calcular_costo` permite calcular el valor con diferentes combinaciones de duración, impuesto y descuento. En Python esto permite ofrecer variantes de uso mediante argumentos opcionales.

## 7. Manejo de excepciones

El proyecto incluye:

- Excepciones personalizadas en `excepciones.py`.
- Bloques `try/except` para capturar errores.
- Bloques `try/except/else` para separar el manejo de errores de las operaciones exitosas.
- Bloques `try/except/finally` para garantizar acciones de cierre y registro.
- Encadenamiento de excepciones mediante `raise ... from error`.
- Registro de eventos y errores en `logs/software_fj.log`.

## 8. Operaciones simuladas

El archivo `main.py` ejecuta 16 operaciones, entre ellas:

1. Registro válido de clientes.
2. Registro de un cliente con correo inválido.
3. Intento de registro duplicado.
4. Creación correcta de los tres tipos de servicios.
5. Intento de creación de un servicio con tarifa negativa.
6. Creación y confirmación de reservas.
7. Intento de confirmar una reserva cuando el servicio no está disponible.
8. Aplicación de descuento e impuesto.
9. Cancelación de una reserva.
10. Intento de confirmar una reserva inexistente.

## 9. Consideraciones

- No se utiliza una base de datos.
- Los clientes, servicios y reservas permanecen en memoria mientras se ejecuta el programa.
- El archivo de logs conserva el registro de eventos y errores.
- Los métodos de cálculo reciben valores opcionales para aplicar impuestos y descuentos.
