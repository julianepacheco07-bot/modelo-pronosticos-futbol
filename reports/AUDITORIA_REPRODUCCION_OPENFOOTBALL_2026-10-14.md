# Auditoría de reproducción OpenFootball — 14 de octubre de 2026

## Resultado de la ejecución

- Ejecución GitHub Actions: [#4](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38576799121)
- Commit ejecutado: `318bdf5453e84e3aaa5393aa9905cb19724935d7`
- Estado del workflow: éxito.
- Artefacto: `backtest-openfootball-4` (Excel, manifiesto y JSON fuente).
- Fuentes recuperadas: 15/15 (cinco ligas × tres temporadas), sin errores de descarga.
- Filas fuente: 5.256.
- Filas con marcadores utilizables: 5.235.
- Filas sin marcador usable: 21.
- Duplicados exactos: 0.
- Conflictos de marcador por fixture: 0.
- Partidos limpios: 5.235.
- Partidos evaluables: 4.883.
- Omitidos por no tener cinco partidos previos para ambos equipos: 352.

## Resultados globales del script actual

| Modelo | N | Exactitud | Brier | LogLoss |
|---|---:|---:|---:|---:|
| Multiplicadores 1.10/0.90 | 4.883 | 48,76 % | 0,618848 | 1,030323 |
| Neutral 1.00/1.00 | 4.883 | 47,76 % | 0,627266 | 1,042172 |
| Ajuste local/visitante | 4.883 | 48,49 % | 0,619985 | 1,033296 |

No hay cuotas históricas verificadas; EV y ROI no se calculan. Estos resultados por sí solos no demuestran rentabilidad.

## Filas sin marcador usable

Las 21 filas se distribuyen así:
- LaLiga 2024-25: 10.
- Serie A 2024-25: 10.
- Ligue 1 2025-26: 1.

Se conservan en la hoja `Invalidos` y en `Datos_fuente`; no entran al cálculo de métricas. Antes de una auditoría definitiva, contrastar estos registros con otra fuente confiable y no completar marcadores por inferencia.

## Comparación con el informe histórico agregado

El libro anterior `Backtest_Multitemporada_Modelo_Futbol_Resultados.xlsx` reportaba N=4.770 y, para el modelo 1.10/0.90, exactitud 52,935 %, Brier 0,593680 y LogLoss 0,995944. La ejecución actual reporta N=4.883, exactitud 48,761 %, Brier 0,618848 y LogLoss 1,030323.

La diferencia es de 113 partidos evaluados. Aunque el informe histórico no conserva predicciones fila por fila suficientes para una conciliación fixture a fixture, no es válido atribuir la diferencia a una causa única. Cambiaron al menos el parser y el conjunto de filas evaluables, y el informe agregado previo no permite comparar las mismas predicciones. Por tanto, los resultados antiguos y nuevos **no son directamente comparables** y no debe declararse que la discrepancia histórica está resuelta.

## Limitaciones metodológicas pendientes

1. El script limita la distribución de Poisson a goles 0–10 y renormaliza las probabilidades truncadas; la auditoría anterior documentó un límite distinto. Debe fijarse un método único y medir sensibilidad.
2. El script usa los cinco partidos previos por equipo y exige al menos cinco observaciones para ambos; se deben congelar y documentar las reglas antes de comparar versiones.
3. No hay cuotas históricas, así que no hay análisis de valor esperado ni ROI.
4. Las fuentes remotas pueden cambiar. El manifiesto registra URL, SHA-256 y tamaño, pero para repetir exactamente el experimento deben archivarse los JSON y reutilizarse los mismos hashes.
5. La ejecución automática verifica que el script termine y publique archivos, no que las métricas sean correctas. Se necesitan pruebas automáticas de calidad de datos y reconciliación.

## Dictamen

La reproducción automatizada **se ejecuta y produce artefactos**, y recupera las 15 fuentes. La calidad básica de datos es auditable. Sin embargo, la validación estadística y la conciliación contra el informe histórico siguen pendientes. No usar estas métricas como evidencia de rentabilidad ni afirmar que el modelo está validado.
