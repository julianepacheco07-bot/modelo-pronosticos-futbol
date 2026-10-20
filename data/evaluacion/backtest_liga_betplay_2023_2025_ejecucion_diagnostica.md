# Backtest diagnóstico corregido — Liga BetPlay 2023–2025

**Estado: análisis exploratorio; recalibración no aprobada.**  
**Cobertura de la fuente consultada:** 2023–2025 parcial; el archivo 2025 recuperado llega a mayo.

## Correcciones aplicadas al código

- El parser ahora acepta líneas de partido con y sin hora de inicio. La versión anterior omitía encuentros sin hora.
- Se normalizan algunos alias conocidos: Alianza Petrolera/Alianza FC y Atlético Junior/Junior.
- Se detectan duplicados después de normalizar los alias.
- Las predicciones se agrupan por fecha: ningún resultado de un partido del mismo día se añade al historial hasta que todas las predicciones de esa fecha están generadas. La fuente no ofrece horas de inicio fiables para ordenar encuentros dentro del día.
- Se añadió una comparación con una línea base de frecuencias históricas acumuladas, suavizadas y calculadas solo con resultados anteriores.

## Cobertura y muestra

| Fuente | Marcadores parseados |
|---|---:|
| 2023 | 452 |
| 2024 | 432 |
| 2025 (parcial) | 167 |
| **Total** | **1.051** |

- Duplicados tras normalización de alias: **0**.
- Equipos normalizados identificados: **23**.
- Predicciones evaluadas: **995**.
- Período de predicciones: **18 de febrero de 2023 a 4 de mayo de 2025**.

Fuentes: [2023](https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2023_co1.txt), [2024](https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2024_co1.txt), [2025](https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2025_co1.txt).

## Modelo frente a línea base rolling

| Mercado | Brier modelo | Brier base | Log loss modelo | Log loss base | Prob. media modelo | Frecuencia observada |
|---|---:|---:|---:|---:|---:|---:|
| 1X2 multiclase | 0,6256 | 0,6379 | 1,0399 | 1,0569 | — | — |
| Over 1.5 | 0,2343 | 0,2321 | 0,6623 | 0,6571 | 65,98 % | 63,72 % |
| Under 3.5 | 0,1474 | 0,1454 | 0,4723 | 0,4667 | 80,48 % | 82,41 % |
| Ambos marcan | 0,2506 | 0,2488 | 0,6943 | 0,6907 | 44,49 % | 44,42 % |

Para 1X2, el modelo tiene una exactitud de **47,34 %** y la línea base **47,14 %**; el pequeño aumento de exactitud no reemplaza la comparación de probabilidades con Brier y Log loss.

## Conclusión

El Poisson mejora a la línea base en Brier y Log loss para 1X2, pero la línea base es mejor en los tres mercados de goles evaluados. Por ahora, **no se debe recalibrar ni aprobar el modelo para recomendaciones automáticas**. La diferencia es pequeña y no se calcularon intervalos de confianza.

## Pendientes antes de aprobar

1. Auditar manualmente una muestra de fechas, resultados y fases del torneo.
2. Completar la normalización histórica de nombres de clubes.
3. Calcular calibración por bandas e intervalos de confianza mediante remuestreo temporal.
4. Evaluar por separado Apertura, Finalización, cuadrangulares y playoffs.
5. Incorporar cuotas prepartido verificadas capturadas antes del inicio para estudiar valor esperado; no se calcula ROI con esta fuente.

No hay evidencia aquí de rentabilidad, ni se han cambiado los umbrales de apuesta.