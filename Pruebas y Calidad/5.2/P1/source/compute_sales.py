"""
Compute Sales - Actividad 5.2.

Calcula el costo total de todas las ventas usando un catálogo de precios (JSON)
y un registro de ventas (JSON). Cumple con el enunciado y archivos de apoyo A5.2.

Formato catálogo: lista de objetos con "title" y "price".
Formato ventas: lista de objetos con "Product" y "Quantity".

Invocación: python computeSales.py priceCatalogue.json salesRecord.json
"""

import json
import os
import sys
import time


def load_json_file(file_path):
    """
    Carga un archivo JSON.

    Args:
        file_path: Ruta al archivo JSON.

    Returns:
        Datos parseados (list o dict) o None si hay error.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: '{file_path}'")
        return None
    except json.JSONDecodeError as err:
        print(f"Error: JSON inválido en '{file_path}': {err}")
        return None
    except PermissionError:
        print(f"Error: Sin permiso para leer: '{file_path}'")
        return None


def build_catalogue_from_product_list(raw_data):
    """
    Construye diccionario producto -> precio desde el catálogo del apoyo A5.2.

    Formato: lista de objetos con "title" y "price".

    Args:
        raw_data: Lista o estructura cargada del JSON del catálogo.

    Returns:
        Dict título (str) -> precio (float). Entradas inválidas se reportan.
    """
    catalogue = {}
    if raw_data is None:
        return catalogue

    if not isinstance(raw_data, list):
        print("Error catálogo: se esperaba una lista de productos.")
        return catalogue

    for idx, item in enumerate(raw_data):
        if not isinstance(item, dict):
            print(f"Error catálogo: entrada [{idx}] no es un objeto.")
            continue
        title = item.get("title")
        price = item.get("price")
        if title is None:
            print(f"Error catálogo: falta 'title' en producto [{idx}].")
            continue
        if price is None:
            print(f"Error catálogo: falta 'price' para '{title}'.")
            continue
        try:
            catalogue[str(title)] = float(price)
        except (TypeError, ValueError):
            print(f"Error catálogo: precio no numérico para '{title}'.")

    return catalogue


def iter_sales_items(raw_sales):
    """
    Itera sobre cada ítem de venta del registro A5.2.

    Formato: lista de objetos con "Product" y "Quantity".

    Args:
        raw_sales: Lista cargada del JSON de ventas.

    Yields:
        Tuplas (producto, cantidad).
    """
    if raw_sales is None:
        return

    if not isinstance(raw_sales, list):
        print("Error ventas: se esperaba una lista de ventas.")
        return

    for idx, row in enumerate(raw_sales):
        if not isinstance(row, dict):
            print(f"Error ventas: fila [{idx}] no es un objeto.")
            continue
        product = row.get("Product") or row.get("product")
        quantity = row.get("Quantity") or row.get("quantity")
        if product is None:
            print(f"Error ventas: falta 'Product' en fila [{idx}].")
            continue
        try:
            qty = int(quantity) if quantity is not None else 1
            if qty < 0:
                qty = 0
        except (TypeError, ValueError):
            print(f"Error ventas: 'Quantity' inválida en fila [{idx}].")
            continue
        yield (str(product), qty)


def compute_total_cost(catalogue, raw_sales):
    """
    Calcula el costo total y el detalle por ítem.

    Args:
        catalogue: Dict producto -> precio.
        raw_sales: Lista de ventas (JSON cargado).

    Returns:
        Tupla (costo_total, lista de (producto, cantidad, precio, subtotal)).
    """
    total = 0.0
    details = []

    for product, quantity in iter_sales_items(raw_sales):
        price = catalogue.get(product)
        if price is None:
            print(f"Advertencia: producto '{product}' no está en el catálogo; se omite.")
            details.append((product, quantity, None, None))
            continue
        subtotal = price * quantity
        total += subtotal
        details.append((product, quantity, price, subtotal))

    return (total, details)


def format_results(total, details, elapsed_seconds):
    """
    Genera líneas de resultado legibles (pantalla y archivo).

    Args:
        total: Costo total.
        details: Lista de (producto, cantidad, precio, subtotal).
        elapsed_seconds: Tiempo de ejecución en segundos.

    Returns:
        Lista de cadenas.
    """
    lines = [
        "=" * 60,
        "RESULTADOS DE VENTAS",
        "=" * 60,
        "",
        "Detalle por ítem:",
        "-" * 60
    ]

    for product, quantity, price, subtotal in details:
        if price is None:
            lines.append(f"  {product}: cantidad {quantity} (no en catálogo)")
        else:
            lines.append(f"  {product}: {quantity} x {price:.2f} = {subtotal:.2f}")

    lines.extend([
        "-" * 60,
        f"TOTAL: {total:.2f}",
        "",
        f"Tiempo de ejecución: {elapsed_seconds:.6f} segundos",
        "=" * 60
    ])
    return lines


def main():
    """Punto de entrada. Uso: python computeSales.py priceCatalogue.json salesRecord.json"""
    if len(sys.argv) < 3:
        print("Uso: python computeSales.py priceCatalogue.json salesRecord.json")
        sys.exit(1)

    catalogue_path = sys.argv[1]
    sales_path = sys.argv[2]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "results", "SalesResults.txt")

    start_time = time.time()

    raw_catalogue = load_json_file(catalogue_path)
    raw_sales = load_json_file(sales_path)

    if raw_catalogue is None or raw_sales is None:
        sys.exit(1)

    catalogue = build_catalogue_from_product_list(raw_catalogue)
    if not catalogue:
        print("Error: El catálogo está vacío o es inválido.")
        sys.exit(1)

    total, details = compute_total_cost(catalogue, raw_sales)
    elapsed = time.time() - start_time

    lines = format_results(total, details, elapsed)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as out:
        for line in lines:
            out.write(line + "\n")

    for line in lines:
        print(line)


if __name__ == "__main__":
    main()
