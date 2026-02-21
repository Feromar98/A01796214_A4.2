"""
Script para ejecutar todas las pruebas unitarias.

Ejecuta todas las pruebas y genera un reporte de cobertura.
"""

import unittest
import sys
import os

# Agregar el directorio source al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

if __name__ == '__main__':
    # Descubrir y ejecutar todas las pruebas
    loader = unittest.TestLoader()
    suite = loader.discover(os.path.dirname(__file__), pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Salir con código de error si hay fallos
    sys.exit(0 if result.wasSuccessful() else 1)
