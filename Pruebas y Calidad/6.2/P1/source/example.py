"""
Ejemplo de uso del sistema de reservas.

Este script demuestra cómo usar las clases del sistema de reservas.
"""

import os
from reservation_system import ReservationSystem


def main():
    """Función principal que demuestra el uso del sistema."""
    # Crear directorio para datos si no existe
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
    os.makedirs(data_dir, exist_ok=True)

    # Inicializar el sistema
    system = ReservationSystem(data_dir)

    print("=== Sistema de Reservas - Ejemplo de Uso ===\n")

    # Crear clientes
    print("1. Creando clientes...")
    system.create_customer('C001', 'Juan Pérez', 'juan@example.com', '555-0101')
    system.create_customer('C002', 'María García', 'maria@example.com', '555-0102')
    print("   ✓ Clientes creados\n")

    # Crear hoteles
    print("2. Creando hoteles...")
    system.create_hotel('H001', 'Hotel Plaza', 'Ciudad de México', 20)
    system.create_hotel('H002', 'Hotel Beach', 'Cancún', 15)
    print("   ✓ Hoteles creados\n")

    # Mostrar información
    print("3. Información del Hotel H001:")
    system.display_hotel('H001')
    print()

    print("4. Información del Cliente C001:")
    system.display_customer('C001')
    print()

    # Crear reservaciones
    print("5. Creando reservaciones...")
    system.create_reservation('R001', 'C001', 'H001', '2024-06-01', '2024-06-05')
    system.create_reservation('R002', 'C002', 'H002', '2024-06-10', '2024-06-15')
    print("   ✓ Reservaciones creadas\n")

    # Mostrar información actualizada del hotel
    print("6. Información actualizada del Hotel H001:")
    system.display_hotel('H001')
    print()

    # Mostrar información de reservación
    print("7. Información de la Reservación R001:")
    system.display_reservation('R001')
    print()

    # Cancelar una reservación
    print("8. Cancelando reservación R001...")
    system.cancel_reservation('R001')
    print("   ✓ Reservación cancelada\n")

    # Mostrar información final del hotel
    print("9. Información final del Hotel H001:")
    system.display_hotel('H001')
    print()

    print("=== Ejemplo completado ===")
    print(f"Los datos se guardaron en: {data_dir}")


if __name__ == '__main__':
    main()
