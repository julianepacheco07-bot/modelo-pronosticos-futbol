# Backtest temporal — línea base Poisson

- **Ejecución:** 18 de octubre de 2026 (UTC).
- **Estado:** backtest exploratorio; no demuestra rentabilidad.
- **Periodo:** temporadas 2023-24, 2024-25 y 2025-26.
- **Ligas:** Premier League, LaLiga, Serie A, Bundesliga y Ligue 1.
- **Método:** rolling-origin; usa únicamente partidos anteriores, hasta los últimos 10 por equipo, exige al menos 5 previos por equipo y suaviza tasas hacia la media histórica de goles de la liga.

## Cobertura

| Indicador | Resultado |
|---|---:|
| Partidos completos cargados | 5.235 |
| Partidos evaluados fuera de muestra | 4.883 |
| Omitidos por historial insuficiente | 352 |
| Errores de descarga | 0 |

## Métricas

| Mercado | N | Brier | Log loss | Resultado adicional |
|---|---:|---:|---:|---|
| 1X2 | 4.883 | 0,620000 | 1,033273 | Exactitud: 49,72% |
| Más de 1.5 goles | 4.883 | 0,171989 | 0,526403 | Prob. media: 76,68%; frecuencia real: 77,66% |
| Menos de 3.5 goles | 4.883 | 0,210731 | 0,611270 | Prob. media: 68,35%; frecuencia real: 68,67% |
| Ambos marcan: sí | 4.883 | 0,246733 | 0,686673 | Prob. media: 55,97%; frecuencia real: 55,05% |

**Lectura crítica:** las medias previstas de Over 1.5, Under 3.5 y Ambos marcan se aproximan a las frecuencias observadas agregadas, pero eso no demuestra calibración por rangos ni ventaja frente a una línea base simple. La exactitud 1X2 de 49,72% tampoco es suficiente para concluir calidad sin comparación con modelos de referencia y desglose por liga/temporada.

## Limitaciones

- No se usaron cuotas, por lo que no se calcula EV ni ROI.
- Las probabilidades provienen de una línea base Poisson sencilla, sin ajustes de fuerza de equipo, alineaciones ni lesiones.
- La liquidación anticipada de “ganar o liderar por 2 goles” no puede validarse con marcadores finales solamente; requiere cronologías históricas de goles.
- El Brier 1X2 es la suma de errores cuadrados de las tres clases.
- El manifiesto de fuentes y resultados está en el JSON asociado.

## Archivos

- src/backtest_temporal.py: implementación reproducible.
- data/evaluacion/backtest_temporal_2023_2026.json: métricas, cobertura y limitaciones.
- data/evaluacion/backtest_temporal_2023_2026.md: resumen de resultados.
