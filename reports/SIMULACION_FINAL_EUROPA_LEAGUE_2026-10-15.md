# Simulación Europa League — tabla gerencial revisada — 15/10/2026

## Criterios aplicados
- **Simples:** se evalúan los mercados disponibles y se priorizan por probabilidad; el umbral acordado es 75%. La cuota simple se registra solo cuando hay un precio verificable.
- **Combinadas:** se forman con dos selecciones de partidos distintos. **No se exige cuota combinada verificable para calcular la probabilidad conjunta ni para ordenar las propuestas.** Se multiplica la probabilidad de cada selección como aproximación bajo independencia. El umbral acordado es 65%; si hay varias propuestas, se prioriza la de mayor probabilidad.
- La cuota justa teórica (1/probabilidad conjunta) es una referencia matemática, no la cuota real que ofrece una casa. La cuota real de la combinada puede quedar no disponible sin bloquear la evaluación.

## Tabla de cinco columnas

| Partido | Pronóstico simple | Cuota simple | Combinada de dos selecciones | Cuota combinada |
|---|---|---|---|---|
| Sparta Praha vs Lillestrøm | Más de 1.5 goles (80.96%) | No verificada | Sparta Praha–Lillestrøm: Más de 1.5 + Lech Poznań–Leverkusen: Más de 1.5 (67.67%) | No requerida; cuota real no verificada |
| AZ Alkmaar vs Hapoel Beer-Sheva | Menos de 3.5 goles (75.04%) | No verificada | — | — |
| Salzburg vs Milan | Menos de 3.5 goles (75.19%) | No verificada | — | — |
| Lech Poznań vs Leverkusen | Más de 1.5 goles (83.58%) | No verificada | — | — |
| Celje vs Omonia | Menos de 3.5 goles (74.47%) | No verificada | — | — |
| Lyon vs Crystal Palace | Más de 1.5 goles (77.61%) | No verificada | — | — |
| Union SG vs Real Sociedad | Más de 1.5 goles (77.61%) | No verificada | — | — |
| Torreense vs Sunderland | Más de 1.5 goles (76.86%) | No verificada | — | — |
| Benfica vs Celtic | Más de 1.5 goles (75.09%) | No verificada | — | — |
| Bournemouth vs Sturm Graz | Más de 1.5 goles (74.48%) | No verificada | — | — |
| Celta Vigo vs Juventus | Menos de 3.5 goles (76.06%) | No verificada | — | — |
| Dinamo Zagreb vs Anderlecht | Menos de 3.5 goles (74.47%) | No verificada | — | — |
| Ferencváros vs Viktoria Plzeň | Más de 1.5 goles (79.48%) | No verificada | — | — |
| Hoffenheim vs Beşiktaş | Más de 1.5 goles (78.73%) | No verificada | — | — |
| Jagiellonia vs Ararat-Armenia | Más de 1.5 goles (80.96%) | No verificada | — | — |
| Marseille vs Olympiacos | Más de 1.5 goles (80.96%) | No verificada | — | — |
| NEC Nijmegen vs Levski Sofia | Más de 1.5 goles (75.86%) | No verificada | — | — |
| Rennes vs OFI Crete | Menos de 3.5 goles (76.61%) | No verificada | — | — |

## Combinada prioritaria
1. **Sparta Praha vs Lillestrøm — Más de 1.5 goles:** 80.96%.
2. **Lech Poznań vs Leverkusen — Más de 1.5 goles:** 83.58%.
3. **Probabilidad conjunta estimada:** **67.67%**, supera el umbral de 65%.
4. **Cuota justa teórica:** **1.48**.
5. **Cuota combinada real:** no disponible/no verificada; no se necesita para evaluar la combinación según el acuerdo metodológico.

Otras combinadas alcanzan el umbral, y quedan registradas para trazabilidad en el archivo CSV. La propuesta prioritaria tiene la mayor probabilidad conjunta (67.67%); hay otras empatadas en ese valor.

## Evaluación de simples y cuotas
No se encontró confirmación directa suficiente de cuotas actuales de Betano Colombia para la lista completa de mercados simples. Por eso, el informe no inventa precios ni EV de simples. Esto **no bloquea las combinadas**, cuyo criterio de selección acordado es probabilístico.

## Límites de la simulación
- Las probabilidades provienen de la rama Poisson exploratoria existente, no de un modelo calibrado y validado específicamente para Europa League.
- Varios equipos tienen historial muy corto dentro de la fuente incorporada, por lo que los porcentajes deben interpretarse con cautela.
- Los partidos son del 15/10/2026; el archivo es la salida de simulación prepartido, no una recomendación para apostar una vez iniciado el encuentro.
- La probabilidad conjunta asume independencia entre partidos; no constituye garantía de acierto.

## Archivos de soporte
- [Probabilidades base de la simulación](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/data/simulacion/simulacion_europa_league_2026-10-15.json)
- [Registro de combinadas y probabilidades conjuntas](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/data/simulacion/combinadas_europa_league_2026-10-15.csv)
- [Evaluación de mercados individuales](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/data/simulacion/evaluacion_mercados_europa_league_2026-10-15.csv)
- [Calendario oficial UEFA](https://www.uefa.com/uefaeuropaleague/news/02a8-2174cafa5bb6-82bbc20c9b92-1000--2026-27-europa-league-all-the-league-phase-fixtures-and-re/).
