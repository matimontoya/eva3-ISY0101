# EVA3 — Observabilidad del agente IA

Este espacio corresponde únicamente al trabajo de la Evaluación Parcial 3. Los archivos de la EVA2 se consultan como referencia y no se modifican.

## Objetivo

Medir el comportamiento del agente en un conjunto controlado de consultas, registrar resultados y visualizar métricas para sustentar hallazgos y recomendaciones.

## Archivos


- `casos_prueba.json`: escenarios y resultados esperados para la evaluación.
- `esquema_eventos.json`: campos propuestos para registrar métricas y trazas.
- `registro_pruebas.csv`: resultados observados durante las consultas manuales.
- `mediciones_recursos.csv` y `registro_recursos.csv`: mediciones de CPU y memoria observadas con Docker.
- `dashboard.py`: genera el tablero HTML desde los CSV.
- `dashboard.html`: visualización generada.

## Actualizar y abrir el dashboard

Desde esta carpeta ejecuta:

```bash
python3 dashboard.py
```

Luego abre `dashboard.html` en un navegador. Cada vez que cambien los CSV, vuelve a ejecutar el generador para actualizar los gráficos. El generador usa solo la biblioteca estándar de Python.

## Alcance

Las métricas reflejan únicamente las ejecuciones anotadas en los CSV y no equivalen a una evaluación general del agente. No se registran preguntas completas, notas, contraseñas ni datos privados.
