"""
Pruebas unitarias para el sistema completo de reservas.

Incluye casos de prueba positivos y negativos para la integración.
"""

import unittest
import os
import tempfile
import shutil
from sys import path

# Agregar el directorio source al path
path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from reservation_system import ReservationSystem


class TestReservationSystem(unittest.TestCase):
    """Pruebas unitarias para ReservationSystem."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.test_dir = tempfile.mkdtemp()
        self.system = ReservationSystem(self.test_dir)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        shutil.rmtree(self.test_dir)

    def test_create_reservation_integration(self):
        """Caso positivo: Crear reservación con cliente y hotel existentes."""
        self.system.create_customer('C001', 'Juan', 'juan@test.com', '123')
        self.system.create_hotel('H001', 'Hotel Test', 'Ciudad', 10)
        result = self.system.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        self.assertTrue(result)

    def test_create_reservation_customer_not_exists(self):
        """Caso negativo: Crear reservación con cliente inexistente."""
        self.system.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        result = self.system.create_reservation(
            'R001', 'C999', 'H001', '2024-01-01', '2024-01-05'
        )
        self.assertFalse(result)

    def test_create_reservation_hotel_not_exists(self):
        """Caso negativo: Crear reservación con hotel inexistente."""
        self.system.create_customer('C001', 'Juan', 'juan@test.com', '123')
        result = self.system.create_reservation(
            'R001', 'C001', 'H999', '2024-01-01', '2024-01-05'
        )
        self.assertFalse(result)

    def test_cancel_reservation_integration(self):
        """Caso positivo: Cancelar reservación completa."""
        self.system.create_customer('C001', 'Juan', 'juan@test.com', '123')
        self.system.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        self.system.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        result = self.system.cancel_reservation('R001')
        self.assertTrue(result)
        # Verificar que la habitación se liberó
        hotel = self.system.hotel_manager.get_hotel('H001')
        self.assertEqual(hotel.available_rooms, 10)

    def test_cancel_reservation_not_exists(self):
        """Caso negativo: Cancelar reservación que no existe."""
        result = self.system.cancel_reservation('R999')
        self.assertFalse(result)

    def test_full_workflow(self):
        """Caso positivo: Flujo completo del sistema."""
        # Crear cliente
        self.assertTrue(self.system.create_customer(
            'C001', 'Juan Pérez', 'juan@test.com', '1234567890'
        ))

        # Crear hotel
        self.assertTrue(self.system.create_hotel(
            'H001', 'Hotel Test', 'Ciudad Test', 5
        ))

        # Crear reservación
        self.assertTrue(self.system.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        ))

        # Verificar que la habitación se reservó
        hotel = self.system.hotel_manager.get_hotel('H001')
        self.assertEqual(hotel.available_rooms, 4)
        self.assertIn('R001', hotel.reservations)

        # Cancelar reservación
        self.assertTrue(self.system.cancel_reservation('R001'))

        # Verificar que la habitación se liberó
        hotel = self.system.hotel_manager.get_hotel('H001')
        self.assertEqual(hotel.available_rooms, 5)
        self.assertNotIn('R001', hotel.reservations)


if __name__ == '__main__':
    unittest.main()
