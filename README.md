# Pruebas y Calidad - Repositorio de Programas

Estructura organizada para gestionar programas, pruebas y evidencias de ejecución exitosa.

## Estructura del repositorio

```
Pruebas y Calidad/
├── 4.2/
│   ├── P1/
│   │   ├── source/   # Código fuente
│   │   ├── tests/    # Casos de prueba
│   │   └── results/  # Evidencia de corridas exitosas
│   ├── P2/
│   │   ├── source/
│   │   ├── tests/
│   │   └── results/
│   └── P3/
│       ├── source/
│       ├── tests/
│       └── results/
├── 5.2/
│   └── P1/
│       ├── source/
│       ├── tests/
│       └── results/
└── 6.2/
    └── P1/
        ├── source/
        ├── tests/
        └── results/
```

## Uso de las carpetas

- **source**: Código fuente de cada programa
- **tests** / **test**: Casos de prueba
- **results**: Evidencia de ejecuciones exitosas (capturas, logs, salidas del programa)

## Actividad 4.2 - Ejercicios de Programación

### P1 - Compute Statistics
Calcula estadísticas descriptivas (media, mediana, moda, desviación estándar poblacional, varianza poblacional).

```bash
cd "Pruebas y Calidad/4.2/P1/source"
python compute_statistics.py ../tests/TC1.txt
# O múltiples archivos para formato tabular consolidado:
python compute_statistics.py ../tests/TC1.txt ../tests/TC2.txt ../tests/TC3.txt
```

Salida: `results/StatisticsResults.txt` (formato: TC, COUNT, MEAN, MEDIAN, MODE, SD, VARIANCE)

### P2 - Convert Numbers
Convierte números a representación binaria y hexadecimal.

```bash
cd "Pruebas y Calidad/4.2/P2/source"
python convert_numbers.py ../tests/TC1.txt
# O todos los TCs: python convert_numbers.py ../tests/TC1.txt ../tests/TC2.txt ../tests/TC3.txt ../tests/TC4.txt
```

Salida: `results/ConvertionResults.txt` (formato: ITEM, TCn, BIN, HEX)

### P3 - Word Count
Cuenta la frecuencia de cada palabra en un archivo de texto.

```bash
cd "Pruebas y Calidad/4.2/P3/source"
python word_count.py ../tests/TC1.txt
# Genera results/TC1.Results.txt (y TC2.Results.txt con TC2.txt, etc.)
```

Salida: `results/{TC}.Results.txt` (ej: TC1.Results.txt). Casos de prueba: `tests/TC1.txt` - `TC5.txt`

### Verificación con Pylint
```bash
pip install pylint
cd "Pruebas y Calidad/4.2/P1/source"
pylint compute_statistics.py
```
