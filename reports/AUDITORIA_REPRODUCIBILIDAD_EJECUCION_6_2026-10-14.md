# Auditoría de reproducibilidad y conciliación — ejecución 6

Fecha de ejecución: 2026-10-14.  
Workflow: [Backtest reproducible OpenFootball #6](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38577508580)  
Commit ejecutado: `2ef5647c43e9c216bcbb64ecd11d13019a69b964`  
Artefacto: `backtest-openfootball-6`, SHA-256 del ZIP: `8bce9852bc4ec2ee4846d8fcfb7b52eee7dd690bc316c019931a3c57c505e5ce`  
Vencimiento del artefacto: 2027-01-12.

## Estado de ejecución y pruebas

- Workflow finalizó con éxito.
- Instalación de dependencias: éxito.
- Pruebas unitarias `tests/test_backtest_openfootball.py`: éxito.
- Backtest: éxito.
- Artefacto de resultados y fuentes: publicado.
- Las pruebas cubren normalización de Poisson (0–12), normalización 1X2, duplicados exactos y conflictos de marcadores.

## Reconciliación de datos

| Control | Resultado |
|---|---:|
| Fuentes JSON | 15/15 sin error |
| Filas fuente | 5.256 |
| Marcadores completos antes de limpieza | 5.235 |
| Filas sin marcador usable | 21 |
| Duplicados exactos | 0 |
| Conflictos de marcador | 0 |
| Partidos limpios | 5.235 |
| Evaluables | 4.883 |
| Omitidos por historial insuficiente | 352 |

Las 21 filas sin marcador usable se conservan en `Invalidos`; no se imputan ni entran en las métricas. Los JSON fuente y sus hashes SHA-256 están en el artefacto y en las hojas `Fuentes` y `Datos_fuente`. El artefacto de GitHub Actions expira a los 90 días; descargarlo y archivarlo si se requiere conservación a largo plazo.

## Métricas de la ejecución 6

| Modelo | N | Exactitud | Brier | LogLoss |
|---|---:|---:|---:|---:|
| Multiplicadores 1,10/0,90 | 4.883 | 48,80 % | 0,618848 | 1,030323 |
| Neutral 1,00/1,00 | 4.883 | 47,96 % | 0,627266 | 1,042172 |
| Ajuste local/visitante | 4.883 | 48,78 % | 0,619985 | 1,033297 |

No se calcula EV ni ROI porque no existen cuotas históricas verificadas en los datos disponibles.

## Hallazgo clave: discrepancia histórica no resuelta

El archivo histórico `Backtest_Multitemporada_Modelo_Futbol_Resultados.xlsx` registra 4.770 partidos: 1.510 de 2023-24, 1.665 de 2024-25 y 1.595 de 2025-26. La ejecución actual registra 4.883: 1.510, 1.665 y 1.708 respectivamente. La diferencia de 113 partidos está concentrada en 2025-26.

Además, aun en temporadas con igual tamaño de muestra, las métricas históricas y actuales difieren. Ejemplo: Premier League 2024-25, N=366 en ambos, pero la exactitud anterior del modelo 1,10/0,90 era 53,01 % y la actual es 46,99 %. Por tanto, la discrepancia no es solo una diferencia de conteo: hay diferencias de implementación, de datos históricos usados o de reglas del modelo que no están reconciliadas.

Los libros históricos disponibles no incluyen todas las predicciones originales fila por fila, por lo que no permiten una comparación exacta de cada pronóstico anterior. No se debe presentar la versión actual como equivalente a la anterior.

## Decisión recomendada

1. Marcar la ejecución técnica como reproducible a nivel de código, fuente identificada y artefacto generado.
2. Marcar la validación estadística y la equivalencia con el informe antiguo como **PENDIENTES**.
3. No seleccionar una versión ganadora ni hacer afirmaciones de rentabilidad hasta comparar los mismos fixtures con el mismo algoritmo y los mismos parámetros.
4. Próxima tarea técnica: crear un evaluador de comparación fixture-a-fixture y una especificación canónica del algoritmo; luego ejecutar el mismo conjunto congelado con ambas implementaciones. Si no se recupera la predicción original por partido, la comparación histórica exacta seguirá siendo imposible y se deberá declarar una nueva línea base desde esta versión.

## Dictamen

La automatización funciona y las pruebas actuales pasan, pero las pruebas no demuestran por sí solas ausencia de fuga temporal ni corrección estadística integral. La calidad de datos básica queda documentada; la conciliación histórica, calibración y evaluación de rentabilidad permanecen abiertas.
