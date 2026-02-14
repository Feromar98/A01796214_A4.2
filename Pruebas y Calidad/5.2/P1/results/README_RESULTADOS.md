# Actividad 5.2 P1 - Resultados (archivos de apoyo A5.2)

## Archivos de prueba (A5.2 Archivos de Apoyo)

- **TC1.ProductList.json**: Catálogo de precios (lista de objetos con `title` y `price`).
- **TC1.Sales.json**, **TC2.Sales.json**, **TC3.Sales.json**: Registros de ventas (lista de objetos con `Product` y `Quantity`).
- **Results_expected.txt**: Totales de referencia del enunciado (TC1, TC2, TC3).

## Invocación (según enunciado)

```bash
cd "Pruebas y Calidad/5.2/P1/source"
python computeSales.py ../tests/TC1.ProductList.json ../tests/TC1.Sales.json
python computeSales.py ../tests/TC1.ProductList.json ../tests/TC2.Sales.json
python computeSales.py ../tests/TC1.ProductList.json ../tests/TC3.Sales.json
```

## Resultados

- **SalesResults.txt**: Salida legible de la última ejecución (detalle por ítem, TOTAL, tiempo).
- **Results.txt**: Totales por TC en formato del enunciado (TOTAL).
- TC1 coincide con el valor de referencia: **2481.86**.

## Verificación Flake8 y Pylint

```bash
pip install flake8 pylint
cd "Pruebas y Calidad/5.2/P1/source"
flake8 compute_sales.py --max-line-length=100
pylint compute_sales.py
```
