"""
Pruebas unitarias para la clase Reservation y ReservationManager.

Incluye casos de prueba positivos y negativos.
"""

import unittest
import os
import json
import tempfile
import shutil
from sys import path

# Agregar el directorio source al path
path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from reservation import Reservation, ReservationManager


class TestReservation(unittest.TestCase):
    """Pruebas unitarias para la clase Reservation."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.reservation = Reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )

    def test_reservation_creation(self):
        """Caso positivo: Crear una reservación válida."""
        self.assertEqual(self.reservation.reservation_id, 'R001')
        self.assertEqual(self.reservation.customer_id, 'C001')
        self.assertEqual(self.reservation.hotel_id, 'H001')
        self.assertEqual(self.reservation.check_in, '2024-01-01')
        self.assertEqual(self.reservation.check_out, '2024-01-05')
        self.assertEqual(self.reservation.status, 'active')

    def test_reservation_to_dict(self):
        """Caso positivo: Convertir reservación a diccionario."""
        res_dict = self.reservation.to_dict()
        self.assertIsInstance(res_dict, dict)
        self.assertEqual(res_dict['reservation_id'], 'R001')
        self.assertEqual(res_dict['status'], 'active')

    def test_reservation_from_dict(self):
        """Caso positivo: Crear reservación desde diccionario válido."""
        data = {
            'reservation_id': 'R002',
            'customer_id': 'C002',
            'hotel_id': 'H002',
            'check_in': '2024-02-01',
            'check_out': '2024-02-05',
            'status': 'active'
        }
        reservation = Reservation.from_dict(data)
        self.assertIsNotNone(reservation)
        self.assertEqual(reservation.reservation_id, 'R002')

    def test_reservation_from_dict_invalid(self):
        """Caso negativo: Crear reservación desde diccionario inválido."""
        data = {'invalid': 'data'}
        reservation = Reservation.from_dict(data)
        self.assertIsNone(reservation)

    def test_reservation_display_info(self):
        """Caso positivo: Mostrar información de la reservación."""
        info = self.reservation.display_info()
        self.assertIn('R001', info)
        self.assertIn('C001', info)

    def test_reservation_cancel(self):
        """Caso positivo: Cancelar una reservación."""
        result = self.reservation.cancel()
        self.assertTrue(result)
        self.assertEqual(self.reservation.status, 'cancelled')

    def test_reservation_cancel_already_cancelled(self):
        """Caso negativo: Cancelar reservación ya cancelada."""
        self.reservation.cancel()
        result = self.reservation.cancel()
        self.assertFalse(result)

    def test_reservation_is_valid_date_range(self):
        """Caso positivo: Validar rango de fechas válido."""
        self.assertTrue(self.reservation.is_valid_date_range())

    def test_reservation_invalid_date_range(self):
        """Caso negativo: Validar rango de fechas inválido."""
        invalid_reservation = Reservation(
            'R002', 'C001', 'H001', '2024-01-05', '2024-01-01'
        )
        self.assertFalse(invalid_reservation.is_valid_date_range())

    def test_reservation_invalid_date_format(self):
        """Caso negativo: Validar formato de fecha inválido."""
        invalid_reservation = Reservation(
            'R002', 'C001', 'H001', 'invalid-date', '2024-01-05'
        )
        self.assertFalse(invalid_reservation.is_valid_date_range())


class TestReservationManager(unittest.TestCase):
    """Pruebas unitarias para la clase ReservationManager."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'reservations.json')
        self.manager = ReservationManager(self.test_file)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        shutil.rmtree(self.test_dir)

    def test_create_reservation(self):
        """Caso positivo: Crear una reservación."""
        result = self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        self.assertTrue(result)
        self.assertIn('R001', self.manager.reservations)

    def test_create_reservation_duplicate(self):
        """Caso negativo: Crear reservación con ID duplicado."""
        self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        result = self.manager.create_reservation(
            'R001', 'C002', 'H002', '2024-02-01', '2024-02-05'
        )
        self.assertFalse(result)

    def test_create_reservation_invalid_date_range(self):
        """Caso negativo: Crear reservación con rango de fechas inválido."""
        result = self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-05', '2024-01-01'
        )
        self.assertFalse(result)

    def test_create_reservation_same_dates(self):
        """Caso negativo: Crear reservación con fechas iguales."""
        result = self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-01'
        )
        self.assertFalse(result)

    def test_cancel_reservation(self):
        """Caso positivo: Cancelar una reservación."""
        self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        result = self.manager.cancel_reservation('R001')
        self.assertTrue(result)
        self.assertEqual(self.manager.reservations['R001'].status, 'cancelled')

    def test_cancel_reservation_not_exists(self):
        """Caso negativo: Cancelar reservación que no existe."""
        result = self.manager.cancel_reservation('R999')
        self.assertFalse(result)

    def test_display_reservation(self):
        """Caso positivo: Mostrar información de una reservación."""
        self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        result = self.manager.display_reservation('R001')
        self.assertTrue(result)

    def test_display_reservation_not_exists(self):
        """Caso negativo: Mostrar reservación que no existe."""
        result = self.manager.display_reservation('R999')
        self.assertFalse(result)

    def test_load_reservations_invalid_json(self):
        """Caso negativo: Cargar archivo JSON inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('invalid json content')
        manager = ReservationManager(self.test_file)
        self.assertEqual(len(manager.reservations), 0)

    def test_load_reservations_invalid_format(self):
        """Caso negativo: Cargar archivo con formato inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([1, 2, 3], f)
        manager = ReservationManager(self.test_file)
        self.assertEqual(len(manager.reservations), 0)

    def test_save_and_load_reservations(self):
        """Caso positivo: Guardar y cargar reservaciones."""
        self.manager.create_reservation(
            'R001', 'C001', 'H001', '2024-01-01', '2024-01-05'
        )
        self.manager.create_reservation(
            'R002', 'C002', 'H002', '2024-02-01', '2024-02-05'
        )

        # Crear nuevo manager para cargar desde archivo
        new_manager = ReservationManager(self.test_file)
        self.assertIn('R001', new_manager.reservations)
        self.assertIn('R002', new_manager.reservations)
        self.assertEqual(new_manager.reservations['R001'].customer_id, 'C001')


if __name__ == '__main__':
    unittest.main()
