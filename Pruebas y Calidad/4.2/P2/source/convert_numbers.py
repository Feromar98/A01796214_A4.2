"""
Convert Numbers - Actividad 4.2 Ejercicio 2.

Este programa lee datos numéricos de un archivo y convierte cada número
a representación binaria y hexadecimal usando algoritmos básicos
sin librerías externas.

Invocación: python convert_numbers.py archivo_con_datos.txt
"""

import os
import sys
import time

# Dígitos hexadecimales para conversión (0-15 mapeados a caracteres)
HEX_DIGITS = "0123456789ABCDEF"


def to_binary(number):
    """
    Convierte entero a cadena binaria usando algoritmo de división básico.

    Maneja números negativos usando representación en complemento a dos.

    Args:
        number: Valor entero a convertir (puede ser negativo).

    Returns:
        Representación en cadena binaria (ej., "1010").
    """
    if number == 0:
        return "0"

    # Para números negativos: usar complemento a dos
    if number < 0:
        # Encontrar bits mínimos necesarios: siguiente potencia de 2 mayor a abs(num)
        abs_val = abs(number)
        bits = 4
        while (1 << bits) <= abs_val:
            bits += 4  # Usar alineación de nibble
        number = (1 << bits) + number

    binary_chars = []
    n = number

    while n > 0:
        remainder = n % 2
        binary_chars.append(str(remainder))
        n = n // 2

    # Invertir para orden correcto
    return ''.join(reversed(binary_chars))


def to_hexadecimal(number):
    """
    Convierte entero a cadena hexadecimal usando algoritmo de división básico.

    Maneja números negativos usando representación en complemento a dos.

    Args:
        number: Valor entero a convertir (puede ser negativo).

    Returns:
        Representación en cadena hexadecimal (ej., "1A2F").
    """
    if number == 0:
        return "0"

    # Para números negativos: usar complemento a dos (igual que binario)
    if number < 0:
        abs_val = abs(number)
        bits = 4
        while (1 << bits) <= abs_val:
            bits += 4
        number = (1 << bits) + number

    hex_chars = []
    n = number

    while n > 0:
        remainder = n % 16
        hex_chars.append(HEX_DIGITS[remainder])
        n = n // 16

    return ''.join(reversed(hex_chars))


def read_numeric_data(file_path):
    """
    Lee datos numéricos de un archivo, manejando entradas inválidas.

    Args:
        file_path: Ruta al archivo con datos numéricos (uno por línea).

    Returns:
        Lista de tuplas (número_línea, número o None, línea_original).
        Las líneas inválidas tienen None como número.
    """
    data = []
    line_number = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line_number += 1
                stripped_line = line.strip()

                if not stripped_line:
                    continue

                try:
                    # Verificar si es número decimal
                    if '.' in stripped_line:
                        num = float(stripped_line)
                        # Convertir a int para conversión de base (truncar)
                        num = int(num)
                    else:
                        num = int(stripped_line)
                    data.append((line_number, num, stripped_line))
                except ValueError:
                    data.append((line_number, None, stripped_line))

    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Sin permiso para leer archivo '{file_path}'.")
        sys.exit(1)

    return data


def _get_tc_name(file_path):
    """Extrae nombre del TC del nombre del archivo (ej: TC1.txt -> TC1)."""
    base = os.path.basename(file_path)
    name, _ = os.path.splitext(base)
    return name


def main():
    """Punto de entrada principal del programa de conversión de números."""
    if len(sys.argv) < 2:
        print("Uso: python convert_numbers.py archivo1.txt [archivo2.txt ...]")
        sys.exit(1)

    # Archivos de entrada (uno o varios)
    input_files = sys.argv[1:]
    # Escribir salida en carpeta results (mismo nivel que source)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "..", "results", "ConvertionResults.txt")

    # Iniciar cronometraje
    start_time = time.time()

    all_sections = []

    for input_file in input_files:
        tc_name = _get_tc_name(input_file)
        data = read_numeric_data(input_file)

        # Procesar conversiones (formato: ITEM, TCn, BIN, HEX)
        results = []
        item_num = 1

        for line_number, number, original in data:
            if number is None:
                print(f"Error: Dato inválido en línea {line_number}: '{original}'")
                results.append(f"{item_num}\t{original}\t#VALUE!\t#VALUE!")
            else:
                binary_str = to_binary(number)
                hex_str = to_hexadecimal(number)
                results.append(f"{item_num}\t{number}\t{binary_str}\t{hex_str}")
                item_num += 1

        header = f"ITEM\t{tc_name}\tBIN\tHEX"
        section = [header] + results
        all_sections.append(section)

    # Finalizar cronometraje
    elapsed_time = time.time() - start_time

    # Concatenar todas las secciones con líneas en blanco entre TCs
    output_lines = []
    for i, section in enumerate(all_sections):
        if i > 0:
            output_lines.extend(["", "", ""])
        output_lines.extend(section)

    output_lines.append("")
    output_lines.append(f"TIME ELAPSED\t{elapsed_time:.6f} seconds")

    # Escribir en archivo
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in output_lines:
            file.write(line + '\n')

    # Imprimir en consola
    for line in output_lines:
        print(line)


if __name__ == "__main__":
    main()
