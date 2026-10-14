# Estado actualizado de reproducción

**Fecha:** 2026-10-14

## Progreso
- [x] Se inspeccionaron los reportes históricos disponibles.
- [x] Se consultaron los 15 JSON de OpenFootball para cinco ligas y tres temporadas.
- [x] Se regeneró un backtest exploratorio: 5.256 filas fuente, 5.122 con marcador final completo, 4.770 evaluables y 352 omitidos por historial insuficiente.
- [x] Se añadieron métricas globales y por temporada a `reports/RESULTADO_REPRODUCCION_2026-10-14.md`.
- [x] Se incorporó `src/backtest_openfootball.py` para repetir la descarga, limpieza, cálculo y generación de Excel desde los JSON.
- [ ] Comparar predicción por predicción con el artefacto exacto que produjo el reporte previo.
- [ ] Explicar la diferencia entre 5.235 reportados antes y 5.122 completos en la fuente consultada actualmente.
- [ ] Verificar calibración contra una línea base adecuada.
- [ ] Obtener cuotas históricas auténticas antes de evaluar EV/ROI.

## Advertencias
El código anterior intentaba descargar CSV de DataHub y no pudo hacerlo en este entorno. La ejecución de esta fecha utilizó directamente OpenFootball JSON; los reportes deben indicar esa fuente real. Los conteos y métricas anteriores no se consideran reconciliados hasta comparar los mismos archivos y las predicciones por partido.

No se afirma rentabilidad ni se recomiendan apuestas a partir de estas métricas.
