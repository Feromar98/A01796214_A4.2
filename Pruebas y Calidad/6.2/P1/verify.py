"""
Script de verificación para el sistema de reservas.

Verifica que el código cumple con los requisitos de la actividad 6.2.
"""

import subprocess
import sys
import os


def run_command(command, cwd=None):
    """Ejecuta un comando y retorna el resultado."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def main():
    """Función principal de verificación."""
    print("=== Verificación del Sistema de Reservas ===\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    source_dir = os.path.join(base_dir, 'source')
    tests_dir = os.path.join(base_dir, 'tests')

    errors = []
    warnings = []

    # 1. Verificar flake8
    print("1. Verificando flake8...")
    success, stdout, stderr = run_command(
        'flake8 *.py --max-line-length=100',
        cwd=source_dir
    )
    if success:
        print("   ✓ flake8: Sin errores\n")
    else:
        print(f"   ✗ flake8 encontró errores:\n{stdout}\n")
        errors.append("flake8")

    # 2. Verificar pylint (solo advertencias, no errores críticos)
    print("2. Verificando pylint...")
    success, stdout, stderr = run_command(
        'pylint --disable=C0103,C0111,R0903,R0913 *.py',
        cwd=source_dir
    )
    # pylint puede retornar código de salida diferente de 0 incluso con warnings
    if "E" in stdout or "F" in stdout:
        print(f"   ⚠ pylint encontró problemas:\n{stdout}\n")
        warnings.append("pylint")
    else:
        print("   ✓ pylint: Sin errores críticos\n")

    # 3. Ejecutar pruebas unitarias
    print("3. Ejecutando pruebas unitarias...")
    success, stdout, stderr = run_command(
        'python run_tests.py',
        cwd=tests_dir
    )
    if success:
        print("   ✓ Todas las pruebas pasaron\n")
    else:
        print(f"   ✗ Algunas pruebas fallaron:\n{stdout}\n")
        errors.append("pruebas unitarias")

    # 4. Verificar cobertura (si está instalado)
    print("4. Verificando cobertura de código...")
    success, stdout, stderr = run_command('coverage --version')
    if success:
        run_command(
            'coverage run --source=source -m unittest discover tests',
            cwd=base_dir
        )
        success, stdout, stderr = run_command(
            'coverage report',
            cwd=base_dir
        )
        print(f"   {stdout}\n")
        if "TOTAL" in stdout:
            # Extraer porcentaje de cobertura
            lines = stdout.split('\n')
            for line in lines:
                if 'TOTAL' in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            coverage = int(parts[-1].rstrip('%'))
                            if coverage >= 85:
                                print(f"   ✓ Cobertura: {coverage}% (>= 85%)\n")
                            else:
                                print(f"   ⚠ Cobertura: {coverage}% (< 85%)\n")
                                warnings.append(f"cobertura: {coverage}%")
                        except ValueError:
                            pass
    else:
        print("   ⚠ coverage no está instalado. Instalar con: pip install coverage\n")
        warnings.append("coverage no instalado")

    # Resumen
    print("=== Resumen ===")
    if not errors and not warnings:
        print("✓ Todas las verificaciones pasaron correctamente")
        return 0
    else:
        if errors:
            print(f"✗ Errores encontrados: {', '.join(errors)}")
        if warnings:
            print(f"⚠ Advertencias: {', '.join(warnings)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
