"""
Pruebas unitarias para la clase Customer y CustomerManager.

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

from customer import Customer, CustomerManager


class TestCustomer(unittest.TestCase):
    """Pruebas unitarias para la clase Customer."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.customer = Customer('C001', 'Juan Pérez', 'juan@test.com', '1234567890')

    def test_customer_creation(self):
        """Caso positivo: Crear un cliente válido."""
        self.assertEqual(self.customer.customer_id, 'C001')
        self.assertEqual(self.customer.name, 'Juan Pérez')
        self.assertEqual(self.customer.email, 'juan@test.com')
        self.assertEqual(self.customer.phone, '1234567890')

    def test_customer_to_dict(self):
        """Caso positivo: Convertir cliente a diccionario."""
        customer_dict = self.customer.to_dict()
        self.assertIsInstance(customer_dict, dict)
        self.assertEqual(customer_dict['customer_id'], 'C001')
        self.assertEqual(customer_dict['name'], 'Juan Pérez')

    def test_customer_from_dict(self):
        """Caso positivo: Crear cliente desde diccionario válido."""
        data = {
            'customer_id': 'C002',
            'name': 'María García',
            'email': 'maria@test.com',
            'phone': '0987654321'
        }
        customer = Customer.from_dict(data)
        self.assertIsNotNone(customer)
        self.assertEqual(customer.customer_id, 'C002')
        self.assertEqual(customer.name, 'María García')

    def test_customer_from_dict_invalid(self):
        """Caso negativo: Crear cliente desde diccionario inválido."""
        data = {'invalid': 'data'}
        customer = Customer.from_dict(data)
        self.assertIsNone(customer)

    def test_customer_display_info(self):
        """Caso positivo: Mostrar información del cliente."""
        info = self.customer.display_info()
        self.assertIn('C001', info)
        self.assertIn('Juan Pérez', info)

    def test_customer_modify_info(self):
        """Caso positivo: Modificar información del cliente."""
        result = self.customer.modify_info(
            name='Juan Carlos Pérez',
            email='juancarlos@test.com'
        )
        self.assertTrue(result)
        self.assertEqual(self.customer.name, 'Juan Carlos Pérez')
        self.assertEqual(self.customer.email, 'juancarlos@test.com')


class TestCustomerManager(unittest.TestCase):
    """Pruebas unitarias para la clase CustomerManager."""

    def setUp(self):
        """Configuración inicial para cada prueba."""
        self.test_dir = tempfile.mkdtemp()
        self.test_file = os.path.join(self.test_dir, 'customers.json')
        self.manager = CustomerManager(self.test_file)

    def tearDown(self):
        """Limpieza después de cada prueba."""
        shutil.rmtree(self.test_dir)

    def test_create_customer(self):
        """Caso positivo: Crear un cliente."""
        result = self.manager.create_customer(
            'C001', 'Juan Pérez', 'juan@test.com', '1234567890'
        )
        self.assertTrue(result)
        self.assertIn('C001', self.manager.customers)

    def test_create_customer_duplicate(self):
        """Caso negativo: Crear cliente con ID duplicado."""
        self.manager.create_customer('C001', 'Juan', 'juan@test.com', '123')
        result = self.manager.create_customer('C001', 'María', 'maria@test.com', '456')
        self.assertFalse(result)

    def test_create_customer_empty_name(self):
        """Caso negativo: Crear cliente con nombre vacío."""
        result = self.manager.create_customer('C001', '', 'juan@test.com', '123')
        self.assertFalse(result)

    def test_create_customer_empty_name_whitespace(self):
        """Caso negativo: Crear cliente con nombre solo espacios."""
        result = self.manager.create_customer('C001', '   ', 'juan@test.com', '123')
        self.assertFalse(result)

    def test_create_customer_empty_email(self):
        """Caso negativo: Crear cliente con email vacío."""
        result = self.manager.create_customer('C001', 'Juan', '', '123')
        self.assertFalse(result)

    def test_create_customer_empty_email_whitespace(self):
        """Caso negativo: Crear cliente con email solo espacios."""
        result = self.manager.create_customer('C001', 'Juan', '   ', '123')
        self.assertFalse(result)

    def test_delete_customer(self):
        """Caso positivo: Eliminar un cliente."""
        self.manager.create_customer('C001', 'Juan', 'juan@test.com', '123')
        result = self.manager.delete_customer('C001')
        self.assertTrue(result)
        self.assertNotIn('C001', self.manager.customers)

    def test_delete_customer_not_exists(self):
        """Caso negativo: Eliminar cliente que no existe."""
        result = self.manager.delete_customer('C999')
        self.assertFalse(result)

    def test_display_customer(self):
        """Caso positivo: Mostrar información de un cliente."""
        self.manager.create_customer('C001', 'Juan', 'juan@test.com', '123')
        result = self.manager.display_customer('C001')
        self.assertTrue(result)

    def test_display_customer_not_exists(self):
        """Caso negativo: Mostrar cliente que no existe."""
        result = self.manager.display_customer('C999')
        self.assertFalse(result)

    def test_modify_customer(self):
        """Caso positivo: Modificar información de un cliente."""
        self.manager.create_customer('C001', 'Juan', 'juan@test.com', '123')
        result = self.manager.modify_customer('C001', name='Juan Carlos')
        self.assertTrue(result)
        self.assertEqual(self.manager.customers['C001'].name, 'Juan Carlos')

    def test_modify_customer_not_exists(self):
        """Caso negativo: Modificar cliente que no existe."""
        result = self.manager.modify_customer('C999', name='Nuevo')
        self.assertFalse(result)

    def test_load_customers_invalid_json(self):
        """Caso negativo: Cargar archivo JSON inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write('invalid json content')
        manager = CustomerManager(self.test_file)
        self.assertEqual(len(manager.customers), 0)

    def test_load_customers_invalid_format(self):
        """Caso negativo: Cargar archivo con formato inválido."""
        with open(self.test_file, 'w', encoding='utf-8') as f:
            json.dump([1, 2, 3], f)
        manager = CustomerManager(self.test_file)
        self.assertEqual(len(manager.customers), 0)

    def test_save_and_load_customers(self):
        """Caso positivo: Guardar y cargar clientes."""
        self.manager.create_customer('C001', 'Juan', 'juan@test.com', '123')
        self.manager.create_customer('C002', 'María', 'maria@test.com', '456')

        # Crear nuevo manager para cargar desde archivo
        new_manager = CustomerManager(self.test_file)
        self.assertIn('C001', new_manager.customers)
        self.assertIn('C002', new_manager.customers)
        self.assertEqual(new_manager.customers['C001'].name, 'Juan')


if __name__ == '__main__':
    unittest.main()
