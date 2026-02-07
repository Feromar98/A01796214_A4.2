"""
Word Count - Actividad 4.2 Ejercicio 3.

Este programa lee texto de un archivo y cuenta la frecuencia de cada
palabra distinta usando algoritmos básicos sin librerías externas.

Invocación: python word_count.py archivo_con_datos.txt
"""

import os
import sys
import time


def extract_words(line):
    """
    Extrae palabras de una línea, separando por espacios en blanco.

    Args:
        line: Cadena que contiene texto.

    Returns:
        Lista de palabras (cadenas) encontradas en la línea.
    """
    words = []
    current_word = []
    for char in line:
        if char.isspace():
            if current_word:
                words.append(''.join(current_word))
                current_word = []
        else:
            current_word.append(char)
    if current_word:
        words.append(''.join(current_word))
    return words


def read_words_from_file(file_path):
    """
    Lee todas las palabras de un archivo, manejando errores correctamente.

    Args:
        file_path: Ruta al archivo que contiene texto.

    Returns:
        Tupla de (diccionario_frecuencia_palabras, contador_errores).
        Las líneas inválidas se reportan en consola.
    """
    # Diccionario: palabra -> conteo (algoritmo básico, sin Counter)
    word_count = {}
    line_number = 0
    error_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line_number += 1
                stripped_line = line.strip()

                # Saltar líneas vacías (no es error)
                if not stripped_line:
                    continue

                words = extract_words(stripped_line)

                for word in words:
                    # Validar: la palabra debe contener al menos una letra/dígito
                    if not word:
                        continue
                    # Contar la palabra
                    word_count[word] = word_count.get(word, 0) + 1

    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Sin permiso para leer archivo '{file_path}'.")
        sys.exit(1)

    return word_count, error_count


def sort_words_by_frequency_then_name(word_count):
    """
    Ordena palabras por frecuencia (descendente), luego por nombre (ascendente).

    Usa algoritmo de ordenamiento básico - sorted() está permitido como built-in.

    Args:
        word_count: Diccionario que mapea palabra a conteo.

    Returns:
        Lista de tuplas (palabra, conteo), ordenadas.
    """
    return sorted(word_count.items(), key=lambda x: (-x[1], x[0]))


def _get_tc_name(file_path):
    """Extrae nombre del TC del nombre del archivo (ej: TC1.txt -> TC1)."""
    base = os.path.basename(file_path)
    name, _ = os.path.splitext(base)
    return name


def main():
    """Punto de entrada principal del programa de conteo de palabras."""
    if len(sys.argv) < 2:
        print("Uso: python word_count.py archivo_con_datos.txt")
        sys.exit(1)

    # Ruta del archivo desde argumento de línea de comandos
    input_file = sys.argv[1]
    tc_name = _get_tc_name(input_file)
    # Escribir salida en carpeta results: {TC_name}.Results.txt
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "..", "results", f"{tc_name}.Results.txt")

    # Iniciar cronometraje
    start_time = time.time()

    # Leer y contar palabras
    word_count, _ = read_words_from_file(input_file)

    # Ordenar: por frecuencia descendente, luego por palabra ascendente
    sorted_words = sort_words_by_frequency_then_name(word_count)

    # Finalizar cronometraje
    elapsed_time = time.time() - start_time

    # Formato como TC1.Results: Row Labels, Count of TCn, (blank), Grand Total
    header = f"Row Labels\tCount of {tc_name}"
    results = []
    total_count = 0

    for word, count in sorted_words:
        results.append(f"{word}\t{count}")
        total_count += count

    blank_line = "(blank)\t"
    grand_total_line = f"Grand Total\t{total_count}"
    time_line = f"TIME ELAPSED\t{elapsed_time:.6f} seconds"

    output_lines = [header] + results + [blank_line, grand_total_line, time_line]

    # Escribir en archivo
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in output_lines:
            file.write(line + '\n')

    # Imprimir en consola
    for line in output_lines:
        print(line)


if __name__ == "__main__":
    main()
