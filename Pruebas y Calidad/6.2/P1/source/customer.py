"""
Customer class for Reservation System - Actividad 6.2.

Implementa la clase Customer con métodos para crear, eliminar, mostrar
y modificar información de clientes.
"""

import json
import os


class Customer:
    """Clase que representa un cliente en el sistema de reservas."""

    def __init__(self, customer_id, name, email, phone):
        """
        Inicializa un objeto Customer.

        Args:
            customer_id: Identificador único del cliente.
            name: Nombre del cliente.
            email: Correo electrónico del cliente.
            phone: Teléfono del cliente.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone

    def to_dict(self):
        """
        Convierte el cliente a diccionario para serialización JSON.

        Returns:
            Diccionario con los datos del cliente.
        """
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Customer desde un diccionario.

        Args:
            data: Diccionario con los datos del cliente.

        Returns:
            Objeto Customer o None si hay error.
        """
        try:
            return Customer(
                customer_id=data.get('customer_id'),
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone')
            )
        except (KeyError, TypeError) as err:
            print(f"Error al crear cliente desde diccionario: {err}")
            return None

    def display_info(self):
        """
        Muestra la información del cliente en consola.

        Returns:
            String con la información formateada del cliente.
        """
        info = (f"Cliente ID: {self.customer_id}\n"
                f"Nombre: {self.name}\n"
                f"Email: {self.email}\n"
                f"Teléfono: {self.phone}")
        print(info)
        return info

    def modify_info(self, name=None, email=None, phone=None):
        """
        Modifica la información del cliente.

        Args:
            name: Nuevo nombre (opcional).
            email: Nuevo correo electrónico (opcional).
            phone: Nuevo teléfono (opcional).

        Returns:
            True si se modificó correctamente, False en caso contrario.
        """
        try:
            if name is not None:
                self.name = name
            if email is not None:
                self.email = email
            if phone is not None:
                self.phone = phone
            return True
        except Exception as err:
            print(f"Error al modificar cliente: {err}")
            return False


class CustomerManager:
    """Gestor de clientes con persistencia en archivos JSON."""

    def __init__(self, file_path='customers.json'):
        """
        Inicializa el gestor de clientes.

        Args:
            file_path: Ruta al archivo JSON de persistencia.
        """
        self.file_path = file_path
        self.customers = {}
        self.load_customers()

    def load_customers(self):
        """Carga los clientes desde el archivo JSON."""
        if not os.path.exists(self.file_path):
            self.customers = {}
            return

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.customers = {}
                    for customer_id, customer_data in data.items():
                        customer = Customer.from_dict(customer_data)
                        if customer:
                            self.customers[customer_id] = customer
                        else:
                            print(f"Error: No se pudo cargar cliente {customer_id}")
                else:
                    print("Error: Formato inválido en archivo de clientes")
                    self.customers = {}
        except json.JSONDecodeError as err:
            print(f"Error: JSON inválido en '{self.file_path}': {err}")
            self.customers = {}
        except FileNotFoundError:
            print(f"Error: Archivo no encontrado: '{self.file_path}'")
            self.customers = {}
        except PermissionError:
            print(f"Error: Sin permiso para leer: '{self.file_path}'")
            self.customers = {}
        except Exception as err:
            print(f"Error inesperado al cargar clientes: {err}")
            self.customers = {}

    def save_customers(self):
        """
        Guarda los clientes en el archivo JSON.

        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        try:
            data = {}
            for customer_id, customer in self.customers.items():
                data[customer_id] = customer.to_dict()

            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)
            return True
        except PermissionError:
            print(f"Error: Sin permiso para escribir: '{self.file_path}'")
            return False
        except Exception as err:
            print(f"Error al guardar clientes: {err}")
            return False

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
        if customer_id in self.customers:
            print(f"Error: El cliente {customer_id} ya existe")
            return False

        try:
            if not name or not name.strip():
                print("Error: El nombre no puede estar vacío")
                return False
            if not email or not email.strip():
                print("Error: El email no puede estar vacío")
                return False

            customer = Customer(customer_id, name, email, phone)
            self.customers[customer_id] = customer
            return self.save_customers()
        except Exception as err:
            print(f"Error al crear cliente: {err}")
            return False

    def delete_customer(self, customer_id):
        """
        Elimina un cliente.

        Args:
            customer_id: ID del cliente a eliminar.

        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        if customer_id not in self.customers:
            print(f"Error: El cliente {customer_id} no existe")
            return False

        try:
            del self.customers[customer_id]
            return self.save_customers()
        except Exception as err:
            print(f"Error al eliminar cliente: {err}")
            return False

    def display_customer(self, customer_id):
        """
        Muestra la información de un cliente.

        Args:
            customer_id: ID del cliente a mostrar.

        Returns:
            True si se mostró correctamente, False en caso contrario.
        """
        if customer_id not in self.customers:
            print(f"Error: El cliente {customer_id} no existe")
            return False

        self.customers[customer_id].display_info()
        return True

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
        if customer_id not in self.customers:
            print(f"Error: El cliente {customer_id} no existe")
            return False

        result = self.customers[customer_id].modify_info(name, email, phone)
        if result:
            return self.save_customers()
        return False

    def get_customer(self, customer_id):
        """
        Obtiene un cliente por su ID.

        Args:
            customer_id: ID del cliente.

        Returns:
            Objeto Customer o None si no existe.
        """
        return self.customers.get(customer_id)
