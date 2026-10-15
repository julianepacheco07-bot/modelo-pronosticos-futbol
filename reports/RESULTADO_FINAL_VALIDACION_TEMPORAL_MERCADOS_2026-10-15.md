# Informe final — Validación temporal de mercados y correcciones
**Fecha de ejecución:** 15 de octubre de 2026  
**Workflow final:** [Backtest Sudamérica #38742161811](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38742161811) — **éxito**  
**Commit ejecutado:** `96fec0f282ddeafaa3bb9b299c9c8c5debf9c841`  
**Artefacto:** `backtest-sudamerica`, ID `11975544397`

## Dictamen ejecutivo

Se completó y volvió a ejecutar el backtest de Colombia Primera A, Brasil Serie A y Argentina Primera para 2023–2025. La ejecución recuperó las nueve fuentes esperadas, ejecutó cuatro pruebas unitarias y generó el artefacto final. Se añadieron métricas por liga-temporada, tablas de calibración por intervalos y una mezcla temporal cuyo peso se ajusta exclusivamente con temporadas anteriores.

**Hallazgo central:** el modelo Poisson de forma reciente, sin mezcla, es peor que una referencia simple basada en la prevalencia histórica de la misma liga en los tres mercados examinados. La mezcla temporal mejora ligeramente Over 1.5 y Ambos marcan en el conjunto de prueba 2024–2025, pero no mejora Under 3.5. Estas mejoras son pequeñas, no prueban una ventaja económica y no justifican afirmar rentabilidad ni recomendar apuestas automáticamente.

Las cuotas históricas siguen excluidas como requisito. Este backtest no calcula ROI.

## Cobertura y calidad de datos

| Indicador | Resultado |
|---|---:|
| Fuentes previstas y recuperadas | 9 de 9 |
| Partidos cargados tras limpieza | 3.181 |
| Predicciones evaluadas | 2.933 |
| Partidos omitidos por historial mínimo | 248 |
| Duplicados exactos eliminados | 0 |
| Encuentros con marcadores contradictorios excluidos | 0 |
| Pruebas unitarias | 4 de 4 aprobadas |

Los archivos fuente y sus hashes están en el manifiesto JSON del artefacto. El periodo de evaluación no incluye la primera temporada (2023) para medir la mezcla, porque no existe una temporada anterior de pronósticos puntuados para ajustar su peso.

## Comparación temporal fuera de muestra

La evaluación principal compara 1.900 partidos de las temporadas 2024 y 2025. El peso de la mezcla se escogió con temporadas estrictamente anteriores al periodo de prueba. Brier y log loss más bajos son mejores.

| Mercado | Modelo Poisson Brier / Log loss | Prevalencia histórica Brier / Log loss | Mezcla temporal Brier / Log loss | Skill Brier vs. referencia |
|---|---:|---:|---:|---:|
| Over 1.5 | 0,235836 / 0,668336 | 0,224326 / 0,640523 | **0,223286 / 0,638204** | +0,46 % |
| Under 3.5 | 0,163251 / 0,518947 | **0,145088 / 0,464630** | 0,145225 / 0,464986 | −0,09 % |
| Ambos marcan — Sí | 0,258474 / 0,714612 | 0,246567 / 0,686269 | **0,246008 / 0,685134** | +0,23 % |

### Exactitud con umbral 0,5

| Mercado | Poisson | Prevalencia histórica | Mezcla temporal |
|---|---:|---:|---:|
| Over 1.5 | 61,63 % | 65,42 % | 65,42 % |
| Under 3.5 | 79,68 % | 82,26 % | 82,26 % |
| Ambos marcan — Sí | 54,53 % | 54,42 % | 55,21 % |

La exactitud por sí sola no basta: debe leerse junto con Brier y log loss. En Under 3.5, por ejemplo, la mezcla no supera a la referencia en las métricas probabilísticas, aunque ambas comparten la misma exactitud al umbral de 0,5.

## Pesos de mezcla seleccionados sin fuga temporal

`alpha_modelo` es el peso del modelo Poisson; el resto se asigna a la prevalencia histórica. Los pesos se eligen con las temporadas previas y se aplican a la temporada siguiente.

| Temporada de prueba | Over 1.5 | Under 3.5 | Ambos marcan |
|---|---:|---:|---:|
| 2024 | 10 % modelo / 90 % referencia | 10 % / 90 % | 25 % / 75 % |
| 2025 | 20 % modelo / 80 % referencia | 5 % / 95 % | 20 % / 80 % |

La selección muestra que el modelo aporta poca información incremental frente a la referencia histórica en esta muestra. Los pesos no deben considerarse definitivos: solo hay dos temporadas de prueba.

## Resultado de los ocho pasos

| Paso | Resultado final |
|---|---|
| 1. Conciliar la base histórica | En Sudamérica se verificó cobertura 9/9, sin duplicados exactos ni conflictos de marcador. La discrepancia de 113 partidos de la línea base europea anterior continúa sin reconciliarse porque faltan los snapshots y predicciones originales por partido. |
| 2. Reproducir el backtest | Ejecución final satisfactoria; fuentes, manifiesto y predicciones quedaron publicados como artefacto. |
| 3. Validación temporal independiente | Se evaluaron las temporadas 2024 y 2025 usando pesos ajustados solo con temporadas anteriores. |
| 4. Calibración | Se generaron intervalos de confiabilidad con número de casos, probabilidad media y frecuencia observada. No se declara calibración satisfactoria; el modelo bruto sigue mostrando peor log loss que la referencia. |
| 5. Comparación de modelos | La comparación detectó que el Poisson aislado es inferior a la prevalencia histórica en los tres mercados. La mezcla temporal mejora marginalmente dos mercados y no el tercero. |
| 6. Robustez | Se generaron métricas por liga y temporada. La mejora agregada es pequeña y no demuestra estabilidad universal entre competiciones. |
| 7. Validación por mercado | Over 1.5, Under 3.5 y Ambos marcan se evaluaron por separado, sin extrapolar resultados entre mercados. |
| 8. Reglas de decisión | Se mantiene separada la evaluación probabilística de la económica. No hay afirmación de EV, ROI ni rentabilidad. Las cuotas históricas no se requieren ni se reconstruyen; el ROI solo se evaluará prospectivamente con cuotas reales registradas y apuestas liquidadas. |

## Correcciones implementadas

1. El proceso exige que estén presentes las nueve fuentes sudamericanas esperadas.
2. Los duplicados exactos se eliminan y los encuentros con marcadores contradictorios se excluyen antes de evaluar.
3. El flujo de CI compila el código y ejecuta cuatro pruebas unitarias antes del backtest. Una primera ejecución de pruebas encontró una fixture sintética con historial insuficiente; se corrigió el caso de prueba y la ejecución posterior pasó las cuatro pruebas.
4. Se añadió una referencia de prevalencia histórica calculada solo con partidos anteriores de la misma liga.
5. Se incorporó una mezcla temporal con ajuste exclusivo en temporadas anteriores, métricas por liga-temporada e intervalos de calibración.
6. La ejecución final de GitHub Actions terminó con éxito y publicó el artefacto.

## Decisión técnica

**No aprobar todavía el Poisson aislado como motor de pronósticos operativos para apuestas.** En la evaluación realizada, sus probabilidades son peores que una referencia histórica sencilla. La mezcla temporal puede conservarse como experimento, no como prueba de ventaja: sus mejoras son muy pequeñas y el resultado de Under 3.5 no supera a la referencia.

Siguiente criterio de aceptación: mantener un registro prospectivo de pronósticos y cuotas actuales verificadas, liquidar las selecciones y evaluar calibración, Brier, log loss y ROI por mercado y liga con una muestra previamente definida. Las cuotas históricas no son una condición para ese trabajo ni para el backtest predictivo.

## Archivos

- [Ejecución final de GitHub Actions](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38742161811)
- [Código del backtest sudamericano](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/src/backtest_sudamerica.py)
- [Pruebas unitarias](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/tests/test_backtest_sudamerica.py)
- [Workflow del backtest](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/.github/workflows/backtest-sudamerica.yml)
