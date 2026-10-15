# Simulación Europa League — revisión de cuotas y estado temporal — 15/10/2026

## Resultado de la comprobación de cuotas
Se buscaron precios en resultados públicos y se consultaron páginas de comparadores. No se obtuvo una captura verificable directamente desde Betano Colombia que permita confirmar los precios para los mercados evaluados. Por tanto, **no se registra ninguna cuota como confirmada de Betano Colombia y no se calcula EV definitivo para apuestas prospectivas**. Se retiró del CSV la referencia de 1.18 que se había anotado para Sparta Praha–Lillestrøm, porque provenía de un agregador y no de una verificación directa en Betano Colombia.

## Estado de la simulación
Las probabilidades de los 18 partidos siguen siendo las de la rama exploratoria Poisson del proyecto. No se han cambiado ni se presentan como calibradas. La tabla de evaluación en CSV incluye los mercados de goles, ambos marcan, 1X2 y doble oportunidad, y separa los casos por debajo del umbral de probabilidad de aquellos que necesitan precio verificable para completar el valor esperado.

## Restricción temporal importante
A la hora de esta revisión, los horarios publicados para los partidos del 15 de octubre ya habían pasado o estaban transcurriendo. Por la regla del proyecto, no se usaron estadísticas en vivo ni resultados de los encuentros del día para fabricar una predicción prepartido. En consecuencia, este archivo sirve como auditoría de la simulación, no como una recomendación para apostar ahora en esos encuentros.

## Combinadas
La pareja exploratoria Lech Poznań–Leverkusen Más de 1.5 goles + Sparta Praha–Lillestrøm Más de 1.5 goles tiene una probabilidad conjunta aproximada de 67.67% bajo independencia. Sin cuotas verificadas de ambas selecciones y sin una cuota combinada publicada por Betano Colombia, **no se puede calcular un EV fiable ni recomendarla como apuesta**.

## Próximo paso técnico
Para cerrar la evaluación económica hace falta una fuente verificable de cuotas de Betano Colombia antes del inicio de cada partido (captura o registro guardado en el momento). Para partidos futuros, registrar automáticamente el precio y la hora de consulta permitirá calcular EV, comparar contra el umbral y seleccionar combinadas sin reconstruir precios históricos inexistentes.

## Fuentes consultadas
- [Oddschecker Colombia — Sparta Praha–Lillestrøm](https://www.oddschecker.com/co/futbol/europa-league/sparta-prague-v-lillestrom) — comparador de mercado; no confirma precio directo de Betano Colombia.
- [Oddschecker Colombia — Union Saint-Gilloise–Real Sociedad](https://www.oddschecker.com/co/futbol/europa-league/union-st-gilloise-v-real-sociedad) — comparador de mercado; no confirma precio directo de Betano Colombia.
- [Oddschecker Colombia — Lyon–Crystal Palace](https://www.oddschecker.com/co/futbol/europa-league/lyon-v-crystal-palace) — comparador de mercado; no confirma precio directo de Betano Colombia.
- [SportyTrader — Sparta Praha–Lillestrøm](https://www.sportytrader.com/es/apuestas/sparta-praga-lillestrom-8786953/) — cuotas agregadas, no captura directa de Betano Colombia.
- [SportyTrader — Lyon–Crystal Palace](https://www.sportytrader.com/es/apuestas/lyon-crystal-palace-8786958/) — cuotas agregadas, no captura directa de Betano Colombia.
- [UEFA — calendario de la Europa League 2026/27](https://www.uefa.com/uefaeuropaleague/news/02a8-2174cafa5bb6-82bbc20c9b92-1000--2026-27-europa-league-all-the-league-phase-fixtures-and-re/).
- [JSON original de probabilidades](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/data/simulacion/simulacion_europa_league_2026-10-15.json).
