# Ejecución técnica y estado de reproducción

**Fecha:** 2026-10-14  
**Estado:** código corregido y pruebas básicas ejecutadas; backtest completo pendiente de datos descargados.

## Cambios incorporados al repositorio

- `src/ejecutar_backtest_multitemporada.py`: script de backtesting con importaciones explícitas para el Excel, manifiesto de fuentes y SHA-256, validación de marcadores, registro de duplicados idénticos, exclusión de partidos con marcadores conflictivos y controles temporales.
- `tests/test_backtest_temporal.py`: pruebas para la suma de probabilidades, duplicados idénticos y conflictos de marcador.
- El script genera un Excel con fuentes, métricas globales y por liga/temporada, detalle de pronósticos, omitidos, duplicados, conflictos, filas inválidas y controles de calidad.

## Pruebas que sí se ejecutaron

La copia de trabajo local pasó la compilación de Python y las pruebas sintéticas de probabilidades y limpieza. Estas pruebas no necesitan descargar partidos y no demuestran que el backtest histórico completo sea correcto.

## Bloqueo actual

El entorno de ejecución no pudo resolver el dominio de DataHub por un error de DNS/conectividad. Por eso no se pudo descargar y recalcular aquí la base de las 15 combinaciones de liga/temporada. No se deben declarar reproducidos los conteos históricos ni las métricas anteriores.

## Cómo continuar

1. Ejecutar el script desde un equipo con conexión a internet, o colocar los 15 CSV originales en `datos_futbol_raw/`.
2. Revisar que las 15 fuentes estén en estado `OK` y verificar sus SHA-256.
3. Revisar los duplicados y conflictos antes de interpretar métricas.
4. Comparar las claves de partidos del nuevo resultado con los reportes anteriores para explicar la discrepancia de 113.
5. Guardar el Excel generado y el manifiesto junto con el commit de código utilizado.
6. No calcular ROI/EV sin cuotas históricas prepartido verificables.

## Advertencia metodológica

El modelo actual es un punto de partida con forma reciente y parámetros fijos. Aunque las pruebas técnicas pasen, su exactitud no equivale a rentabilidad, no garantiza ventaja futura y no basta para recomendar apuestas.
