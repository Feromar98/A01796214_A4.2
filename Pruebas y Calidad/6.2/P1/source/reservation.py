"""
Reservation class for Reservation System - Actividad 6.2.

Implementa la clase Reservation con métodos para crear y cancelar reservas.
"""

import json
import os
from datetime import datetime


class Reservation:
    """Clase que representa una reservación en el sistema."""

    def __init__(self, reservation_id, customer_id, hotel_id, check_in, check_out):
        """
        Inicializa un objeto Reservation.

        Args:
            reservation_id: Identificador único de la reservación.
            customer_id: ID del cliente.
            hotel_id: ID del hotel.
            check_in: Fecha de entrada (formato YYYY-MM-DD).
            check_out: Fecha de salida (formato YYYY-MM-DD).
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = 'active'

    def to_dict(self):
        """
        Convierte la reservación a diccionario para serialización JSON.

        Returns:
            Diccionario con los datos de la reservación.
        """
        return {
            'reservation_id': self.reservation_id,
            'customer_id': self.customer_id,
            'hotel_id': self.hotel_id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': self.status
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Reservation desde un diccionario.

        Args:
            data: Diccionario con los datos de la reservación.

        Returns:
            Objeto Reservation o None si hay error.
        """
        try:
            reservation = Reservation(
                reservation_id=data.get('reservation_id'),
                customer_id=data.get('customer_id'),
                hotel_id=data.get('hotel_id'),
                check_in=data.get('check_in'),
                check_out=data.get('check_out')
            )
            reservation.status = data.get('status', 'active')
            return reservation
        except (KeyError, TypeError) as err:
            print(f"Error al crear reservación desde diccionario: {err}")
            return None

    def display_info(self):
        """
        Muestra la información de la reservación en consola.

        Returns:
            String con la información formateada de la reservación.
        """
        info = (f"Reservación ID: {self.reservation_id}\n"
                f"Cliente ID: {self.customer_id}\n"
                f"Hotel ID: {self.hotel_id}\n"
                f"Check-in: {self.check_in}\n"
                f"Check-out: {self.check_out}\n"
                f"Estado: {self.status}")
        print(info)
        return info

    def cancel(self):
        """
        Cancela la reservación.

        Returns:
            True si se canceló correctamente, False en caso contrario.
        """
        if self.status == 'cancelled':
            print(f"Error: La reservación {self.reservation_id} ya está cancelada")
            return False
        self.status = 'cancelled'
        return True

    def is_valid_date_range(self):
        """
        Valida que la fecha de check-out sea posterior a check-in.

        Returns:
            True si el rango de fechas es válido, False en caso contrario.
        """
        try:
            check_in_date = datetime.strptime(self.check_in, '%Y-%m-%d')
            check_out_date = datetime.strptime(self.check_out, '%Y-%m-%d')
            return check_out_date > check_in_date
        except ValueError:
            return False


class ReservationManager:
    """Gestor de reservaciones con persistencia en archivos JSON."""

    def __init__(self, file_path='reservations.json'):
        """
        Inicializa el gestor de reservaciones.

        Args:
            file_path: Ruta al archivo JSON de persistencia.
        """
        self.file_path = file_path
        self.reservations = {}
        self.load_reservations()

    def load_reservations(self):
        """Carga las reservaciones desde el archivo JSON."""
        if not os.path.exists(self.file_path):
            self.reservations = {}
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.reservations = {}
                    for res_id, res_data in data.items():
                        reservation = Reservation.from_dict(res_data)
                        if reservation:
                            self.reservations[res_id] = reservation
                        else:
                            print(f"Error: No se pudo cargar reservación {res_id}")
                else:
                    print("Error: Formato inválido en archivo de reservaciones")
                    self.reservations = {}
        except json.JSONDecodeError as err:
            print(f"Error: JSON inválido en '{self.file_path}': {err}")
            self.reservations = {}
        except FileNotFoundError:
            print(f"Error: Archivo no encontrado: '{self.file_path}'")
            self.reservations = {}
        except PermissionError:
            print(f"Error: Sin permiso para leer: '{self.file_path}'")
            self.reservations = {}
        except Exception as err:
            print(f"Error inesperado al cargar reservaciones: {err}")
            self.reservations = {}

    def save_reservations(self):
        """
        Guarda las reservaciones en el archivo JSON.

        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        try:
            data = {}
            for res_id, reservation in self.reservations.items():
                data[res_id] = reservation.to_dict()

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: Sin permiso para escribir: '{self.file_path}'")
            return False
        except Exception as err:
            print(f"Error al guardar reservaciones: {err}")
            return False

    def create_reservation(self, reservation_id, customer_id, hotel_id,
                          check_in, check_out):
        """
        Crea una nueva reservación.

        Args:
            reservation_id: Identificador único de la reservación.
            customer_id: ID del cliente.
            hotel_id: ID del hotel.
            check_in: Fecha de entrada (formato YYYY-MM-DD).
            check_out: Fecha de salida (formato YYYY-MM-DD).

        Returns:
            True si se creó correctamente, False en caso contrario.
        """
        if reservation_id in self.reservations:
            print(f"Error: La reservación {reservation_id} ya existe")
            return False

        try:
            reservation = Reservation(
                reservation_id, customer_id, hotel_id, check_in, check_out
            )

            if not reservation.is_valid_date_range():
                print("Error: La fecha de check-out debe ser posterior a check-in")
                return False

            self.reservations[reservation_id] = reservation
            return self.save_reservations()
        except Exception as err:
            print(f"Error al crear reservación: {err}")
            return False

    def cancel_reservation(self, reservation_id):
        """
        Cancela una reservación.

        Args:
            reservation_id: ID de la reservación a cancelar.

        Returns:
            True si se canceló correctamente, False en caso contrario.
        """
        if reservation_id not in self.reservations:
            print(f"Error: La reservación {reservation_id} no existe")
            return False

        result = self.reservations[reservation_id].cancel()
        if result:
            return self.save_reservations()
        return False

    def get_reservation(self, reservation_id):
        """
        Obtiene una reservación por su ID.

        Args:
            reservation_id: ID de la reservación.

        Returns:
            Objeto Reservation o None si no existe.
        """
        return self.reservations.get(reservation_id)

    def display_reservation(self, reservation_id):
        """
        Muestra la información de una reservación.

        Args:
            reservation_id: ID de la reservación a mostrar.

        Returns:
            True si se mostró correctamente, False en caso contrario.
        """
        if reservation_id not in self.reservations:
            print(f"Error: La reservación {reservation_id} no existe")
            return False

        self.reservations[reservation_id].display_info()
        return True
