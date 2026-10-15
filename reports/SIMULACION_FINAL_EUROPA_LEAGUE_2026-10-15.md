# Europa League — simulación prepartido para encuentros aún en curso — 15/10/2026

## Corte y método
Se recuperó la simulación prepartido archivada a las 11:41 UTC del 15 de octubre de 2026, antes del inicio de los diez partidos tardíos. Se utilizó el estado actual únicamente para determinar cuáles encuentros seguían en curso; **no se usaron goles, estadísticas ni eventos en vivo para alterar las probabilidades prepartido**. La cobertura en directo del Guardian marcaba 21:11 CEST y señalaba que los diez partidos tardíos acababan de comenzar.

## Tabla de cinco columnas
Las cuotas recuperadas de la mañana son referencias de los mercados 1X2/doble oportunidad, no del mercado de goles seleccionado. Se conservan con esa aclaración para no cambiar ni inventar el precio del mercado. No se calcula el valor esperado de O1,5/U3,5 usando una cuota de otro mercado.

| Partido | Pronóstico simple prepartido | Cuota simple de referencia guardada en la mañana | Combinada de 2 selecciones | Cuota combinada |
|---|---|---|---|---|
| Benfica–Celtic | Más de 1,5 goles (78,27%) | 1,26 (Benfica gana, 1X2; no es cuota O1,5) | — | No requerida por metodología acordada |
| Bournemouth–Sturm Graz | NO BET — O1,5 bajo umbral (74,52%) | 1,18 (Bournemouth gana, 1X2; no es cuota O1,5) | — | No requerida por metodología acordada |
| Celta Vigo–Juventus | Más de 1,5 goles (79,54%) | 2,22 (Juventus gana, 1X2; no es cuota O1,5) | — | No requerida por metodología acordada |
| Dinamo Zagreb–Anderlecht | Menos de 3,5 goles (78,23%) | 1,278 (1X Dinamo; no es cuota U3,5) | — | No requerida por metodología acordada |
| Ferencváros–Viktoria Plzeň | Más de 1,5 goles (80,81%) | 1,91 (Ferencváros gana, 1X2; no es cuota O1,5) | — | No requerida por metodología acordada |
| Hoffenheim–Beşiktaş | Más de 1,5 goles (78,99%) | 3,50 (Beşiktaş gana, 1X2; no es cuota O1,5) | — | No requerida por metodología acordada |
| Jagiellonia–Ararat-Armenia | Más de 1,5 goles (83,09%) | 1,36 (Jagiellonia gana, 1X2; no es cuota O1,5) | Más de 1,5 goles — 83,09% (combinada principal) | No requerida por metodología acordada |
| Marseille–Olympiacos | Más de 1,5 goles (83,09%) | 1,294 (1X Marseille; no es cuota O1,5) | Más de 1,5 goles — 83,09% (combinada principal) | No requerida por metodología acordada |
| NEC Nijmegen–Levski Sofia | NO BET — O1,5 bajo umbral (74,96%) | 1,85 (NEC gana, 1X2; no es cuota O1,5) | — | No requerida por metodología acordada |
| Rennes–OFI Crete | Menos de 3,5 goles (81,61%) | 1,21 (Rennes gana, 1X2; no es cuota U3,5) | — | No requerida por metodología acordada |

## Combinada prioritaria según probabilidad
1. **Jagiellonia–Ararat-Armenia: Más de 1,5 goles** — 83,09%.
2. **Marseille–Olympiacos: Más de 1,5 goles** — 83,09%.
3. **Probabilidad conjunta aproximada: 69,04%**, suponiendo independencia entre partidos.
4. Umbral del proyecto: 65%; supera el umbral.
5. Cuota combinada real: no requerida para evaluar la probabilidad, según el acuerdo metodológico. Cuota justa teórica: **1,45**, solo referencia matemática, no precio ofrecido.

## Filtros simples
- Pasan el umbral probabilístico del 75%: Benfica O1,5; Celta O1,5; Dinamo U3,5; Ferencváros O1,5; Hoffenheim O1,5; Jagiellonia O1,5; Marseille O1,5; Rennes U3,5.
- No pasan: Bournemouth O1,5 (74,52%) y NEC O1,5 (74,96%). Se aplica el umbral exacto sin redondear para forzar elegibilidad.
- La mayoría de los historiales disponibles en el dataset prepartido tiene solo dos partidos por equipo. La etiqueta es candidata condicional, no validación de rentabilidad.

## Fuentes y trazabilidad
- [JSON prepartido original guardado a las 11:41 UTC](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/7ed17bfca02d83e0f90edff0d1f376a14ba2d7b0/data/simulacion/simulacion_europa_league_2026-10-15.json).
- [Cobertura en directo, usada solo para filtrar encuentros no finalizados](https://www.theguardian.com/football/live/2026/oct/15/bournemouth-v-sturm-graz-benfica-v-celtic-and-more-europa-league-live).
- [Calendario oficial UEFA](https://www.uefa.com/uefaeuropaleague/news/02a8-2174cafa5bb6-82bbc20c9b92-1000--2026-27-europa-league-all-the-league-phase-fixtures-and-re/).
