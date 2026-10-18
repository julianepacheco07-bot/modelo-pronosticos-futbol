# Comparación contra baseline histórico — 18-10-2026

## Diseño
Backtest rolling-origin sobre 4.883 partidos de cinco ligas, temporadas 2023-24 a 2025-26. Se comparó el Poisson exploratorio contra una referencia que usa únicamente frecuencias históricas anteriores de la misma liga. Menor Brier/log loss es mejor. La ejecución automatizada completó correctamente; 5.235 partidos completos cargados, 352 omitidos por historial insuficiente y 0 errores de descarga.

## Resultados agregados

| Mercado | Brier Poisson | Brier baseline | Log loss Poisson | Log loss baseline | Evaluación |
|---|---:|---:|---:|---:|---|
| 1X2 | 0,620000 | 0,652465 | 1,033273 | 1,077885 | Poisson mejora ambas métricas |
| Over 1.5 | 0,171989 | 0,172126 | 0,526403 | 0,527160 | Mejora mínima |
| Under 3.5 | 0,210731 | 0,211984 | 0,611270 | 0,614364 | Mejora pequeña |
| Ambos marcan sí | 0,246733 | 0,246996 | 0,686673 | 0,687134 | Mejora mínima |

## Frecuencia observada y probabilidad media

| Mercado | Prob. media Poisson | Frecuencia real |
|---|---:|---:|
| Over 1.5 | 76,68% | 77,66% |
| Under 3.5 | 68,35% | 68,67% |
| Ambos marcan sí | 55,97% | 55,05% |

## Lectura crítica
- El Poisson supera la referencia histórica agregada en las cuatro métricas comparadas, pero la mejora para Over 1.5, Under 3.5 y Ambos marcan es muy pequeña. No debe interpretarse como ventaja de apuestas.
- 1X2 muestra una mejora mayor en Brier y log loss, pero la exactitud del modelo es 49,72%; requiere validación adicional por liga/temporada y calibración.
- La calibración por rangos muestra desviaciones en grupos pequeños y también en algunos rangos grandes; no se debe interpretar una probabilidad individual como fiable solo por estas métricas agregadas.
- No se calcularon EV, ROI ni rentabilidad: el backtest no usa cuotas históricas.
- Según la decisión del usuario, el mercado «ganar o alcanzar ventaja de dos goles» se medirá prospectivamente desde ahora. No se reconstruirá con resultados antiguos.

## Archivos
- Código: `src/backtest_temporal.py`
- Informe completo generado por CI: [artifact del backtest](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/39137984255)
- JSON con desglose, bins de calibración y resultados por liga/temporada: disponible en el artifact de la ejecución enlazada.
