"""
Reservation System - Actividad 6.2.

Sistema de reservas que integra las clases Hotel, Customer y Reservation.
Proporciona una interfaz unificada para gestionar hoteles, clientes y reservaciones.
"""

import os
from hotel import HotelManager
from customer import CustomerManager
from reservation import ReservationManager


class ReservationSystem:
    """Sistema principal de reservas que integra todos los componentes."""

    def __init__(self, data_dir='.'):
        """
        Inicializa el sistema de reservas.

        Args:
            data_dir: Directorio donde se guardarán los archivos JSON.
        """
        self.data_dir = data_dir
        hotels_file = os.path.join(data_dir, 'hotels.json')
        customers_file = os.path.join(data_dir, 'customers.json')
        reservations_file = os.path.join(data_dir, 'reservations.json')

        self.hotel_manager = HotelManager(hotels_file)
        self.customer_manager = CustomerManager(customers_file)
        self.reservation_manager = ReservationManager(reservations_file)

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
        return self.hotel_manager.create_hotel(hotel_id, name, location, rooms)

    def delete_hotel(self, hotel_id):
        """
        Elimina un hotel.

        Args:
            hotel_id: ID del hotel a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        return self.hotel_manager.delete_hotel(hotel_id)

    def display_hotel(self, hotel_id):
        """
        Muestra la información de un hotel.

        Args:
            hotel_id: ID del hotel a mostrar.

        Returns:
            True si se mostró correctamente, False en caso contrario.
        """
        return self.hotel_manager.display_hotel(hotel_id)

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
        return self.hotel_manager.modify_hotel(hotel_id, name, location, rooms)

    def create_customer(self, customer_id, name, email, phone):
        """
        Crea un nuevo cliente.

        Args:
            customer_id: Identificador único del cliente.
            name: Nombre del cliente.
            email: Correo electrónico del cliente.
            phone: Teléfono del cliente.

        Returns:
            True si se creó correctamente, False en caso contrario.
        """
        return self.customer_manager.create_customer(customer_id, name, email, phone)

    def delete_customer(self, customer_id):
        """
        Elimina un cliente.

        Args:
            customer_id: ID del cliente a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        return self.customer_manager.delete_customer(customer_id)

    def display_customer(self, customer_id):
        """
        Muestra la información de un cliente.

        Args:
            customer_id: ID del cliente a mostrar.

        Returns:
            True si se mostró correctamente, False en caso contrario.
        """
        return self.customer_manager.display_customer(customer_id)

    def modify_customer(self, customer_id, name=None, email=None, phone=None):
        """
        Modifica la información de un cliente.

        Args:
            customer_id: ID del cliente a modificar.
            name: Nuevo nombre (opcional).
            email: Nuevo correo electrónico (opcional).
            phone: Nuevo teléfono (opcional).

        Returns:
            True si se modificó correctamente, False en caso contrario.
        """
        return self.customer_manager.modify_customer(
            customer_id, name, email, phone
        )

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
        # Validar que el cliente existe
        if not self.customer_manager.get_customer(customer_id):
            print(f"Error: El cliente {customer_id} no existe")
            return False

        # Validar que el hotel existe
        if not self.hotel_manager.get_hotel(hotel_id):
            print(f"Error: El hotel {hotel_id} no existe")
            return False

        # Crear la reservación
        result = self.reservation_manager.create_reservation(
            reservation_id, customer_id, hotel_id, check_in, check_out
        )

        # Si se creó correctamente, reservar la habitación en el hotel
        if result:
            self.hotel_manager.reserve_room(hotel_id, reservation_id)

        return result

    def cancel_reservation(self, reservation_id):
        """
        Cancela una reservación.

        Args:
            reservation_id: ID de la reservación a cancelar.

        Returns:
            True si se canceló correctamente, False en caso contrario.
        """
        reservation = self.reservation_manager.get_reservation(reservation_id)
        if not reservation:
            print(f"Error: La reservación {reservation_id} no existe")
            return False

        # Cancelar en el gestor de reservaciones
        result = self.reservation_manager.cancel_reservation(reservation_id)

        # Si se canceló correctamente, liberar la habitación en el hotel
        if result:
            self.hotel_manager.cancel_reservation(
                reservation.hotel_id, reservation_id
            )

        return result

    def display_reservation(self, reservation_id):
        """
        Muestra la información de una reservación.

        Args:
            reservation_id: ID de la reservación a mostrar.

        Returns:
            True si se mostró correctamente, False en caso contrario.
        """
        return self.reservation_manager.display_reservation(reservation_id)
