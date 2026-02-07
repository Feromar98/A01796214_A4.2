"""
Compute Statistics - Actividad 4.2 Ejercicio 1.

Este programa lee datos numéricos de un archivo y calcula estadísticas
descriptivas (media, mediana, moda, desviación estándar poblacional,
varianza poblacional) usando algoritmos básicos sin librerías externas.

Invocación: python compute_statistics.py archivo_con_datos.txt
"""

import os
import sys
import time


def read_numeric_data(file_path):
    """
    Lee datos numéricos de un archivo, manejando entradas inválidas.

    Args:
        file_path: Ruta al archivo con datos numéricos (uno por línea).

    Returns:
        Lista de números válidos (int o float). Las líneas inválidas se
        reportan en consola pero no detienen la ejecución.
    """
    numbers = []
    line_number = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line_number += 1
                # Eliminar espacios en blanco para validación
                stripped_line = line.strip()

                # Saltar líneas vacías
                if not stripped_line:
                    continue

                try:
                    # Intentar entero primero para números enteros
                    if '.' in stripped_line:
                        num = float(stripped_line)
                    else:
                        num = int(stripped_line)
                    numbers.append(num)
                except ValueError:
                    print(f"Error: Dato inválido en línea {line_number}: '{stripped_line}'")

    except FileNotFoundError:
        print(f"Error: Archivo '{file_path}' no encontrado.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Sin permiso para leer archivo '{file_path}'.")
        sys.exit(1)

    return numbers


def compute_mean(numbers):
    """
    Calcula la media aritmética (promedio) de una lista de números.

    Args:
        numbers: Lista de valores numéricos.

    Returns:
        Valor de la media como float.
    """
    if not numbers:
        return 0.0

    total = 0.0
    for num in numbers:
        total += num

    return total / len(numbers)


def compute_median(numbers):
    """
    Calcula la mediana (valor central) de una lista ordenada.

    Args:
        numbers: Lista de valores numéricos.

    Returns:
        Valor de la mediana. Para cantidad par, retorna promedio de los dos centrales.
    """
    if not numbers:
        return 0.0

    # Crear copia ordenada para preservar datos originales
    sorted_nums = sorted(numbers)
    length = len(sorted_nums)

    if length % 2 == 1:
        # Cantidad impar: elemento central
        return float(sorted_nums[length // 2])
    # Cantidad par: promedio de los dos elementos centrales
    mid_left = sorted_nums[(length // 2) - 1]
    mid_right = sorted_nums[length // 2]
    return (mid_left + mid_right) / 2.0


def compute_mode(numbers):
    """
    Encuentra la moda (valor más frecuente) de una lista.

    Args:
        numbers: Lista de valores numéricos.

    Returns:
        Valor de la moda, o 'N/A' si no existe moda única.
    """
    if not numbers:
        return 'N/A'

    # Contar frecuencia de cada valor usando algoritmo básico
    frequency = {}
    for num in numbers:
        frequency[num] = frequency.get(num, 0) + 1

    max_freq = 0
    mode_value = None
    mode_count = 0

    for value, freq in frequency.items():
        if freq > max_freq:
            max_freq = freq
            mode_value = value
            mode_count = 1
        elif freq == max_freq:
            mode_count += 1

    # Múltiples valores con misma frecuencia máxima = no hay moda única
    if mode_count > 1:
        return 'N/A'

    return mode_value


def compute_variance(numbers, mean):
    """
    Calcula la varianza poblacional: sum((x - media)^2) / n.

    Args:
        numbers: Lista de valores numéricos.
        mean: Media precalculada de la lista.

    Returns:
        Varianza poblacional como float.
    """
    if not numbers:
        return 0.0

    squared_diffs = 0.0
    for num in numbers:
        diff = num - mean
        squared_diffs += diff * diff

    return squared_diffs / len(numbers)


def compute_standard_deviation(variance):
    """
    Calcula la desviación estándar poblacional (raíz cuadrada de la varianza).

    Args:
        variance: Valor de la varianza poblacional.

    Returns:
        Desviación estándar como float.
    """
    if variance <= 0:
        return 0.0

    # Método de Newton para raíz cuadrada (algoritmo básico)
    guess = variance / 2.0
    for _ in range(50):  # Iteraciones para convergencia
        guess = (guess + variance / guess) / 2.0

    return guess


def _get_tc_name(file_path):
    """Extrae nombre del TC del nombre del archivo (ej: TC1.txt -> TC1)."""
    base = os.path.basename(file_path)
    name, _ = os.path.splitext(base)
    return name


def main():
    """Punto de entrada principal del programa de estadísticas."""
    if len(sys.argv) < 2:
        print("Uso: python compute_statistics.py archivo1.txt [archivo2.txt ...]")
        sys.exit(1)

    # Archivos de entrada (uno o varios)
    input_files = sys.argv[1:]
    # Escribir salida en carpeta results (mismo nivel que source)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "..", "results", "StatisticsResults.txt")

    # Iniciar cronometraje
    start_time = time.time()

    # Procesar cada archivo y recopilar estadísticas
    all_stats = []
    tc_names = []

    for input_file in input_files:
        numbers = read_numeric_data(input_file)

        if not numbers:
            print(f"Error: No se encontraron datos válidos en '{input_file}'.")
            continue

        tc_names.append(_get_tc_name(input_file))
        mean = compute_mean(numbers)
        median = compute_median(numbers)
        mode = compute_mode(numbers)
        variance = compute_variance(numbers, mean)
        std_dev = compute_standard_deviation(variance)

        all_stats.append({
            'count': len(numbers),
            'mean': mean,
            'median': median,
            'mode': mode,
            'sd': std_dev,
            'variance': variance
        })

    if not all_stats:
        print("Error: No se procesaron archivos con datos válidos.")
        sys.exit(1)

    # Finalizar cronometraje
    elapsed_time = time.time() - start_time

    # Formato tabular como A4.2.P1.Results-errata: TC\tTC1\tTC2\t...
    header = "TC\t" + "\t".join(tc_names)
    def _fmt_count(val):
        return str(int(val)) if val == int(val) else f"{val:.2f}"

    def _fmt_median(val):
        return str(int(val)) if val == int(val) else str(val)

    count_row = "COUNT\t" + "\t".join(_fmt_count(s['count']) for s in all_stats)
    mean_row = "MEAN\t" + "\t".join(f"{s['mean']:.10g}" for s in all_stats)
    median_row = "MEDIAN\t" + "\t".join(_fmt_median(s['median']) for s in all_stats)
    mode_row = "MODE\t" + "\t".join(str(s['mode']) for s in all_stats)
    sd_row = "SD\t" + "\t".join(f"{s['sd']:.10g}" for s in all_stats)
    variance_row = "VARIANCE\t" + "\t".join(f"{s['variance']:.10g}" for s in all_stats)
    time_row = "TIME ELAPSED\t" + f"{elapsed_time:.6f} seconds"

    results = [
        header,
        count_row,
        mean_row,
        median_row,
        mode_row,
        sd_row,
        variance_row,
        time_row
    ]

    # Escribir en archivo
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in results:
            file.write(line + '\n')

    # Imprimir en consola
    for line in results:
        print(line)


if __name__ == "__main__":
    main()
