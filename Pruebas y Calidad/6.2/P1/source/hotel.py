"""
Hotel class for Reservation System - Actividad 6.2.

Implementa la clase Hotel con métodos para crear, eliminar, mostrar,
modificar información, reservar habitaciones y cancelar reservas.
"""

import json
import os


class Hotel:
    """Clase que representa un hotel en el sistema de reservas."""

    def __init__(self, hotel_id, name, location, rooms):
        """
        Inicializa un objeto Hotel.

        Args:
            hotel_id: Identificador único del hotel.
            name: Nombre del hotel.
            location: Ubicación del hotel.
            rooms: Número total de habitaciones disponibles.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.rooms = rooms
        self.available_rooms = rooms
        self.reservations = []

    def to_dict(self):
        """
        Convierte el hotel a diccionario para serialización JSON.

        Returns:
            Diccionario con los datos del hotel.
        """
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'location': self.location,
            'rooms': self.rooms,
            'available_rooms': self.available_rooms,
            'reservations': self.reservations
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Hotel desde un diccionario.

        Args:
            data: Diccionario con los datos del hotel.

        Returns:
            Objeto Hotel o None si hay error.
        """
        try:
            hotel = Hotel(
                hotel_id=data.get('hotel_id'),
                name=data.get('name'),
                location=data.get('location'),
                rooms=data.get('rooms', 0)
            )
            hotel.available_rooms = data.get('available_rooms', hotel.rooms)
            hotel.reservations = data.get('reservations', [])
            return hotel
        except (KeyError, TypeError) as err:
            print(f"Error al crear hotel desde diccionario: {err}")
            return None

    def display_info(self):
        """
        Muestra la información del hotel en consola.

        Returns:
            String con la información formateada del hotel.
        """
        info = (f"Hotel ID: {self.hotel_id}\n"
                f"Nombre: {self.name}\n"
                f"Ubicación: {self.location}\n"
                f"Habitaciones totales: {self.rooms}\n"
                f"Habitaciones disponibles: {self.available_rooms}\n"
                f"Reservaciones activas: {len(self.reservations)}")
        print(info)
        return info

    def modify_info(self, name=None, location=None, rooms=None):
        """
        Modifica la información del hotel.

        Args:
            name: Nuevo nombre (opcional).
            location: Nueva ubicación (opcional).
            rooms: Nuevo número de habitaciones (opcional).

        Returns:
            True si se modificó correctamente, False en caso contrario.
        """
        try:
            if name is not None:
                self.name = name
            if location is not None:
                self.location = location
            if rooms is not None:
                if rooms < len(self.reservations):
                    print("Error: No se puede reducir habitaciones "
                          "por debajo de las reservadas")
                    return False
                diff = rooms - self.rooms
                self.rooms = rooms
                self.available_rooms += diff
            return True
        except Exception as err:
            print(f"Error al modificar hotel: {err}")
            return False

    def reserve_room(self, reservation_id):
        """
        Reserva una habitación en el hotel.

        Args:
            reservation_id: ID de la reservación.

        Returns:
            True si se reservó correctamente, False en caso contrario.
        """
        if self.available_rooms <= 0:
            print(f"Error: No hay habitaciones disponibles en {self.name}")
            return False
        if reservation_id in self.reservations:
            print(f"Error: La reservación {reservation_id} ya existe")
            return False
        self.reservations.append(reservation_id)
        self.available_rooms -= 1
        return True

    def cancel_reservation(self, reservation_id):
        """
        Cancela una reservación en el hotel.

        Args:
            reservation_id: ID de la reservación a cancelar.

        Returns:
            True si se canceló correctamente, False en caso contrario.
        """
        if reservation_id not in self.reservations:
            print(f"Error: La reservación {reservation_id} no existe")
            return False
        self.reservations.remove(reservation_id)
        self.available_rooms += 1
        return True


class HotelManager:
    """Gestor de hoteles con persistencia en archivos JSON."""

    def __init__(self, file_path='hotels.json'):
        """
        Inicializa el gestor de hoteles.

        Args:
            file_path: Ruta al archivo JSON de persistencia.
        """
        self.file_path = file_path
        self.hotels = {}
        self.load_hotels()

    def load_hotels(self):
        """Carga los hoteles desde el archivo JSON."""
        if not os.path.exists(self.file_path):
            self.hotels = {}
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.hotels = {}
                    for hotel_id, hotel_data in data.items():
                        hotel = Hotel.from_dict(hotel_data)
                        if hotel:
                            self.hotels[hotel_id] = hotel
                        else:
                            print(f"Error: No se pudo cargar hotel {hotel_id}")
                else:
                    print("Error: Formato inválido en archivo de hoteles")
                    self.hotels = {}
        except json.JSONDecodeError as err:
            print(f"Error: JSON inválido en '{self.file_path}': {err}")
            self.hotels = {}
        except FileNotFoundError:
            print(f"Error: Archivo no encontrado: '{self.file_path}'")
            self.hotels = {}
        except PermissionError:
            print(f"Error: Sin permiso para leer: '{self.file_path}'")
            self.hotels = {}
        except Exception as err:
            print(f"Error inesperado al cargar hoteles: {err}")
            self.hotels = {}

    def save_hotels(self):
        """
        Guarda los hoteles en el archivo JSON.

        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        try:
            data = {}
            for hotel_id, hotel in self.hotels.items():
                data[hotel_id] = hotel.to_dict()

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: Sin permiso para escribir: '{self.file_path}'")
            return False
        except Exception as err:
            print(f"Error al guardar hoteles: {err}")
            return False

    def create_hotel(self, hotel_id, name, location, rooms):
        """
        Crea un nuevo hotel.

        Args:
            hotel_id: Identificador único del hotel.
            name: Nombre del hotel.
            location: Ubicación del hotel.
            rooms: Número de habitaciones.

        Returns:
            True si se creó correctamente, False en caso contrario.
        """
        if hotel_id in self.hotels:
            print(f"Error: El hotel {hotel_id} ya existe")
            return False

        try:
            if rooms < 0:
                print("Error: El número de habitaciones debe ser positivo")
                return False

            hotel = Hotel(hotel_id, name, location, rooms)
            self.hotels[hotel_id] = hotel
            return self.save_hotels()
        except Exception as err:
            print(f"Error al crear hotel: {err}")
            return False

    def delete_hotel(self, hotel_id):
        """
        Elimina un hotel.

        Args:
            hotel_id: ID del hotel a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        if hotel_id not in self.hotels:
            print(f"Error: El hotel {hotel_id} no existe")
            return False

        try:
            del self.hotels[hotel_id]
            return self.save_hotels()
        except Exception as err:
            print(f"Error al eliminar hotel: {err}")
            return False

    def display_hotel(self, hotel_id):
        """
        Muestra la información de un hotel.

        Args:
            hotel_id: ID del hotel a mostrar.

        Returns:
            True si se mostró correctamente, False en caso contrario.
        """
        if hotel_id not in self.hotels:
            print(f"Error: El hotel {hotel_id} no existe")
            return False

        self.hotels[hotel_id].display_info()
        return True

    def modify_hotel(self, hotel_id, name=None, location=None, rooms=None):
        """
        Modifica la información de un hotel.

        Args:
            hotel_id: ID del hotel a modificar.
            name: Nuevo nombre (opcional).
            location: Nueva ubicación (opcional).
            rooms: Nuevo número de habitaciones (opcional).

        Returns:
            True si se modificó correctamente, False en caso contrario.
        """
        if hotel_id not in self.hotels:
            print(f"Error: El hotel {hotel_id} no existe")
            return False

        result = self.hotels[hotel_id].modify_info(name, location, rooms)
        if result:
            return self.save_hotels()
        return False

    def reserve_room(self, hotel_id, reservation_id):
        """
        Reserva una habitación en un hotel.

        Args:
            hotel_id: ID del hotel.
            reservation_id: ID de la reservación.

        Returns:
            True si se reservó correctamente, False en caso contrario.
        """
        if hotel_id not in self.hotels:
            print(f"Error: El hotel {hotel_id} no existe")
            return False

        result = self.hotels[hotel_id].reserve_room(reservation_id)
        if result:
            return self.save_hotels()
        return False

    def cancel_reservation(self, hotel_id, reservation_id):
        """
        Cancela una reservación en un hotel.

        Args:
            hotel_id: ID del hotel.
            reservation_id: ID de la reservación a cancelar.

        Returns:
            True si se canceló correctamente, False en caso contrario.
        """
        if hotel_id not in self.hotels:
            print(f"Error: El hotel {hotel_id} no existe")
            return False

        result = self.hotels[hotel_id].cancel_reservation(reservation_id)
        if result:
            return self.save_hotels()
        return False

    def get_hotel(self, hotel_id):
        """
        Obtiene un hotel por su ID.

        Args:
            hotel_id: ID del hotel.

        Returns:
            Objeto Hotel o None si no existe.
        """
        return self.hotels.get(hotel_id)
