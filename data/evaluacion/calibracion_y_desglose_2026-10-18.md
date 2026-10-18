# Paso 1 — calibración y análisis por liga/temporada

**Fecha de ejecución:** 2026-10-18  
**Base:** backtest temporal de 4.883 partidos evaluados en 5 ligas y temporadas 2023-24 a 2025-26.  
**Objetivo:** medir si la línea base Poisson supera la referencia de frecuencias históricas de la liga. Menor Brier y log loss indican menor error probabilístico.

## 1. Resultado agregado

| Mercado | Brier Poisson | Brier referencia | Diferencia (Poisson − referencia) | Log loss Poisson | Log loss referencia |
|---|---:|---:|---:|---:|---:|
| 1X2 | 0,620000 | 0,652465 | -0,032465 | 1,033273 | 1,077885 |
| Over 1.5 | 0,171989 | 0,172126 | -0,000137 | 0,526403 | 0,527160 |
| Under 3.5 | 0,210731 | 0,211984 | -0,001253 | 0,611270 | 0,614364 |
| Ambos marcan sí | 0,246733 | 0,246996 | -0,000263 | 0,686673 | 0,687134 |

El modelo mejora las cuatro métricas agregadas, pero las ventajas en los tres mercados de goles son marginales.

## 2. Calibración por rango

### Over 1.5

| Rango pronosticado | N | Prob. media | Frecuencia real | Diferencia real − prevista |
|---|---:|---:|---:|---:|
| 0,5–0,6 | 35 | 57,84% | 68,57% | +10,73 pp |
| 0,6–0,7 | 751 | 66,71% | 70,44% | +3,73 pp |
| 0,7–0,8 | 2.514 | 75,55% | 76,77% | +1,22 pp |
| 0,8–0,9 | 1.556 | 83,48% | 82,46% | -1,02 pp |
| 0,9–1,0 | 27 | 90,71% | 96,30% | +5,59 pp |

### Under 3.5

| Rango pronosticado | N | Prob. media | Frecuencia real | Diferencia real − prevista |
|---|---:|---:|---:|---:|
| 0,4–0,5 | 112 | 47,03% | 55,36% | +8,33 pp |
| 0,5–0,6 | 690 | 56,15% | 58,84% | +2,69 pp |
| 0,6–0,7 | 1.874 | 65,37% | 65,26% | -0,11 pp |
| 0,7–0,8 | 1.829 | 74,41% | 74,08% | -0,33 pp |
| 0,8–0,9 | 377 | 82,35% | 81,43% | -0,92 pp |
| 0,9–1,0 | 1 | 90,97% | 0,00% | -90,97 pp |

El último rango de Under 3.5 contiene un solo caso y no permite inferencias generales.

### Ambos marcan: sí

| Rango pronosticado | N | Prob. media | Frecuencia real | Diferencia real − prevista |
|---|---:|---:|---:|---:|
| 0,2–0,3 | 1 | 29,98% | 100,00% | +70,02 pp |
| 0,3–0,4 | 46 | 38,23% | 47,83% | +9,60 pp |
| 0,4–0,5 | 950 | 46,55% | 48,21% | +1,66 pp |
| 0,5–0,6 | 2.471 | 55,24% | 54,76% | -0,48 pp |
| 0,6–0,7 | 1.318 | 63,61% | 59,94% | -3,67 pp |
| 0,7–0,8 | 97 | 71,65% | 65,98% | -5,67 pp |

La sobreestimación en rangos de BTTS superiores al 60% es una señal para investigar; los rangos altos tienen menos casos y deben tratarse con cautela.

## 3. Por liga y temporada: Brier Poisson / referencia

| Liga-temporada | N | 1X2 | Over 1.5 | Under 3.5 | Ambos marcan |
|---|---:|---:|---:|---:|---:|
| Premier League 2023-24 | 329 | 0,601709 / 0,639913 | 0,110945 / 0,111728 | 0,246148 / 0,247553 | 0,233719 / 0,237994 |
| Premier League 2024-25 | 366 | 0,612701 / 0,653635 | 0,150244 / 0,152443 | 0,231563 / 0,230679 | 0,245683 / 0,246395 |
| Premier League 2025-26 | 370 | 0,638526 / 0,656930 | 0,166451 / 0,164436 | 0,208306 / 0,211624 | 0,245347 / 0,246174 |
| LaLiga 2023-24 | 329 | 0,622686 / 0,657421 | 0,206299 / 0,203913 | 0,196463 / 0,198714 | 0,251344 / 0,251862 |
| LaLiga 2024-25 | 357 | 0,619576 / 0,650349 | 0,196122 / 0,200746 | 0,177478 / 0,183629 | 0,243969 / 0,249548 |
| LaLiga 2025-26 | 367 | 0,627461 / 0,632319 | 0,170751 / 0,174634 | 0,189374 / 0,189333 | 0,244067 / 0,247135 |
| Serie A 2023-24 | 330 | 0,622400 / 0,660343 | 0,195846 / 0,194036 | 0,192222 / 0,193840 | 0,253024 / 0,250910 |
| Serie A 2024-25 | 355 | 0,617925 / 0,661630 | 0,198151 / 0,196390 | 0,183787 / 0,188407 | 0,253529 / 0,250388 |
| Serie A 2025-26 | 370 | 0,618431 / 0,660266 | 0,210158 / 0,208705 | 0,176656 / 0,173697 | 0,252221 / 0,251036 |
| Bundesliga 2023-24 | 261 | 0,616075 / 0,659327 | 0,128042 / 0,127979 | 0,237534 / 0,243234 | 0,237880 / 0,239183 |
| Bundesliga 2024-25 | 296 | 0,627976 / 0,660902 | 0,155934 / 0,156644 | 0,245814 / 0,245094 | 0,247361 / 0,246324 |
| Bundesliga 2025-26 | 301 | 0,610627 / 0,648671 | 0,136800 / 0,134332 | 0,248864 / 0,245773 | 0,239990 / 0,235626 |
| Ligue 1 2023-24 | 261 | 0,626255 / 0,664177 | 0,190440 / 0,190370 | 0,199092 / 0,200511 | 0,250851 / 0,252547 |
| Ligue 1 2024-25 | 291 | 0,607267 / 0,639025 | 0,144286 / 0,147532 | 0,229158 / 0,231433 | 0,242588 / 0,245690 |
| Ligue 1 2025-26 | 300 | 0,628164 / 0,644248 | 0,203379 / 0,201528 | 0,221130 / 0,219051 | 0,258044 / 0,252075 |

## 4. Interpretación y decisiones

1. **1X2:** Poisson supera la referencia en todas las 15 combinaciones liga-temporada por Brier. Es el resultado más consistente, aunque todavía falta compararlo con probabilidades de mercado sin margen y hacer análisis de incertidumbre.
2. **Over 1.5:** el rendimiento es mixto por liga-temporada, y la mejora agregada es casi nula. No debe asumirse que es el mercado más fuerte solo porque la frecuencia histórica es alta.
3. **Under 3.5:** también mejora de forma agregada, con resultados mixtos por liga-temporada.
4. **Ambos marcan:** mejora agregada muy pequeña y sobreestimación en los rangos 60–80%; no usar todavía esos rangos como señal fuerte.
5. Las métricas agregadas no bastan para seleccionar apuestas. La siguiente validación debe incorporar intervalos de incertidumbre, comparación con cuota de mercado sin margen cuando exista, y evaluación por temporadas separadas.

## 5. Límite acordado para el mercado de ventaja de dos goles

No se estimó ni reconstruyó retrospectivamente ese mercado. A partir de ahora se registrarán antes del inicio: partido, mercado exacto, cuota, hora de captura, fuente y probabilidad del modelo; después del partido: resultado, minuto en que alcanzó ventaja de dos goles si ocurrió, liquidación y evidencia. Solo entonces habrá muestra prospectiva para evaluarlo.
