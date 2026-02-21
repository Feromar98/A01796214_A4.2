"""
Pruebas unitarias para la clase Hotel y HotelManager.

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

from hotel import Hotel, HotelManager


class TestHotel(unittest.TestCase):
    """Pruebas unitarias para la clase Hotel."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.hotel = Hotel('H001', 'Hotel Test', 'Ciudad Test', 10)

    def test_hotel_creation(self):
        """Caso positivo: Crear un hotel válido."""
        self.assertEqual(self.hotel.hotel_id, 'H001')
        self.assertEqual(self.hotel.name, 'Hotel Test')
        self.assertEqual(self.hotel.location, 'Ciudad Test')
        self.assertEqual(self.hotel.rooms, 10)
        self.assertEqual(self.hotel.available_rooms, 10)

    def test_hotel_to_dict(self):
        """Caso positivo: Convertir hotel a diccionario."""
        hotel_dict = self.hotel.to_dict()
        self.assertIsInstance(hotel_dict, dict)
        self.assertEqual(hotel_dict['hotel_id'], 'H001')
        self.assertEqual(hotel_dict['name'], 'Hotel Test')

    def test_hotel_from_dict(self):
        """Caso positivo: Crear hotel desde diccionario válido."""
        data = {
            'hotel_id': 'H002',
            'name': 'Hotel 2',
            'location': 'Ciudad 2',
            'rooms': 5,
            'available_rooms': 5,
            'reservations': []
        }
        hotel = Hotel.from_dict(data)
        self.assertIsNotNone(hotel)
        self.assertEqual(hotel.hotel_id, 'H002')
        self.assertEqual(hotel.name, 'Hotel 2')

    def test_hotel_from_dict_invalid(self):
        """Caso negativo: Crear hotel desde diccionario inválido."""
        data = {'invalid': 'data'}
        hotel = Hotel.from_dict(data)
        self.assertIsNone(hotel)

    def test_hotel_display_info(self):
        """Caso positivo: Mostrar información del hotel."""
        info = self.hotel.display_info()
        self.assertIn('H001', info)
        self.assertIn('Hotel Test', info)

    def test_hotel_modify_info(self):
        """Caso positivo: Modificar información del hotel."""
        result = self.hotel.modify_info(name='Nuevo Nombre', location='Nueva Ciudad')
        self.assertTrue(result)
        self.assertEqual(self.hotel.name, 'Nuevo Nombre')
        self.assertEqual(self.hotel.location, 'Nueva Ciudad')

    def test_hotel_modify_rooms_invalid(self):
        """Caso negativo: Intentar reducir habitaciones por debajo de reservadas."""
        self.hotel.reservations = ['R001', 'R002']
        self.hotel.available_rooms = 8
        result = self.hotel.modify_info(rooms=1)
        self.assertFalse(result)

    def test_hotel_reserve_room(self):
        """Caso positivo: Reservar una habitación."""
        result = self.hotel.reserve_room('R001')
        self.assertTrue(result)
        self.assertEqual(self.hotel.available_rooms, 9)
        self.assertIn('R001', self.hotel.reservations)

    def test_hotel_reserve_room_no_availability(self):
        """Caso negativo: Intentar reservar cuando no hay habitaciones."""
        self.hotel.available_rooms = 0
        result = self.hotel.reserve_room('R001')
        self.assertFalse(result)

    def test_hotel_reserve_room_duplicate(self):
        """Caso negativo: Intentar reservar con ID duplicado."""
        self.hotel.reserve_room('R001')
        result = self.hotel.reserve_room('R001')
        self.assertFalse(result)

    def test_hotel_cancel_reservation(self):
        """Caso positivo: Cancelar una reservación."""
        self.hotel.reserve_room('R001')
        result = self.hotel.cancel_reservation('R001')
        self.assertTrue(result)
        self.assertEqual(self.hotel.available_rooms, 10)
        self.assertNotIn('R001', self.hotel.reservations)

    def test_hotel_cancel_reservation_invalid(self):
        """Caso negativo: Cancelar reservación que no existe."""
        result = self.hotel.cancel_reservation('R999')
        self.assertFalse(result)


class TestHotelManager(unittest.TestCase):
    """Pruebas unitarias para la clase HotelManager."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'hotels.json')
        self.manager = HotelManager(self.test_file)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        shutil.rmtree(self.test_dir)

    def test_create_hotel(self):
        """Caso positivo: Crear un hotel."""
        result = self.manager.create_hotel('H001', 'Hotel Test', 'Ciudad', 10)
        self.assertTrue(result)
        self.assertIn('H001', self.manager.hotels)

    def test_create_hotel_duplicate(self):
        """Caso negativo: Crear hotel con ID duplicado."""
        self.manager.create_hotel('H001', 'Hotel 1', 'Ciudad', 10)
        result = self.manager.create_hotel('H001', 'Hotel 2', 'Ciudad', 5)
        self.assertFalse(result)

    def test_create_hotel_negative_rooms(self):
        """Caso negativo: Crear hotel con número negativo de habitaciones."""
        result = self.manager.create_hotel('H001', 'Hotel', 'Ciudad', -5)
        self.assertFalse(result)

    def test_delete_hotel(self):
        """Caso positivo: Eliminar un hotel."""
        self.manager.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        result = self.manager.delete_hotel('H001')
        self.assertTrue(result)
        self.assertNotIn('H001', self.manager.hotels)

    def test_delete_hotel_not_exists(self):
        """Caso negativo: Eliminar hotel que no existe."""
        result = self.manager.delete_hotel('H999')
        self.assertFalse(result)

    def test_display_hotel(self):
        """Caso positivo: Mostrar información de un hotel."""
        self.manager.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        result = self.manager.display_hotel('H001')
        self.assertTrue(result)

    def test_display_hotel_not_exists(self):
        """Caso negativo: Mostrar hotel que no existe."""
        result = self.manager.display_hotel('H999')
        self.assertFalse(result)

    def test_modify_hotel(self):
        """Caso positivo: Modificar información de un hotel."""
        self.manager.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        result = self.manager.modify_hotel('H001', name='Nuevo Nombre')
        self.assertTrue(result)
        self.assertEqual(self.manager.hotels['H001'].name, 'Nuevo Nombre')

    def test_modify_hotel_not_exists(self):
        """Caso negativo: Modificar hotel que no existe."""
        result = self.manager.modify_hotel('H999', name='Nuevo')
        self.assertFalse(result)

    def test_reserve_room(self):
        """Caso positivo: Reservar habitación."""
        self.manager.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        result = self.manager.reserve_room('H001', 'R001')
        self.assertTrue(result)
        self.assertEqual(self.manager.hotels['H001'].available_rooms, 9)

    def test_reserve_room_hotel_not_exists(self):
        """Caso negativo: Reservar en hotel que no existe."""
        result = self.manager.reserve_room('H999', 'R001')
        self.assertFalse(result)

    def test_cancel_reservation(self):
        """Caso positivo: Cancelar reservación."""
        self.manager.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        self.manager.reserve_room('H001', 'R001')
        result = self.manager.cancel_reservation('H001', 'R001')
        self.assertTrue(result)
        self.assertEqual(self.manager.hotels['H001'].available_rooms, 10)

    def test_cancel_reservation_hotel_not_exists(self):
        """Caso negativo: Cancelar reservación en hotel que no existe."""
        result = self.manager.cancel_reservation('H999', 'R001')
        self.assertFalse(result)

    def test_load_hotels_invalid_json(self):
        """Caso negativo: Cargar archivo JSON inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('invalid json content')
        manager = HotelManager(self.test_file)
        self.assertEqual(len(manager.hotels), 0)

    def test_load_hotels_invalid_format(self):
        """Caso negativo: Cargar archivo con formato inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([1, 2, 3], f)
        manager = HotelManager(self.test_file)
        self.assertEqual(len(manager.hotels), 0)

    def test_save_and_load_hotels(self):
        """Caso positivo: Guardar y cargar hoteles."""
        self.manager.create_hotel('H001', 'Hotel', 'Ciudad', 10)
        self.manager.create_hotel('H002', 'Hotel 2', 'Ciudad 2', 5)

        # Crear nuevo manager para cargar desde archivo
        new_manager = HotelManager(self.test_file)
        self.assertIn('H001', new_manager.hotels)
        self.assertIn('H002', new_manager.hotels)
        self.assertEqual(new_manager.hotels['H001'].name, 'Hotel')


if __name__ == '__main__':
    unittest.main()
