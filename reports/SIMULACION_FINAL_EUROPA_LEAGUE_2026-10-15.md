# Simulación revisada — Europa League — 15/10/2026

## Qué se ha corregido en esta revisión
Se revisaron los 18 partidos y sus probabilidades exploratorias ya calculadas. Para no repetir el error de introducir precios no comprobados, **solo se consigna una cuota concreta en esta versión: Sparta Praha–Lillestrøm, Más de 1.5 goles, 1.18**, encontrada en un comparador que etiqueta el precio como Betano. No equivale a una captura directa de Betano Colombia; hay que comprobarla en la aplicación. Los demás precios quedan vacíos hasta encontrar una fuente verificable. Las cuotas de la versión previa que no tenían verificación suficiente no deben utilizarse.

## Tabla de cinco columnas solicitada

| Partido | Pronóstico simple evaluado | Cuota simple | Estado | Historial del modelo |
|---|---|---:|---|---|
| Sparta Praha vs Lillestrøm | Más de 1.5 goles (80.96%) | 1.18* | NO BET | 1/1 (BAJA) |
| AZ Alkmaar vs Hapoel Beer-Sheva | Menos de 3.5 goles (75.04%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 10/1 (BAJA) |
| Salzburg vs Milan | Menos de 3.5 goles (75.19%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/10 (BAJA) |
| Lech Poznań vs Leverkusen | Más de 1.5 goles (83.58%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/10 (BAJA) |
| Celje vs Omonia | Menos de 3.5 goles (74.47%) | No verificada | NO BET: ningún mercado calculado alcanza 75% | 1/1 (BAJA) |
| Lyon vs Crystal Palace | Más de 1.5 goles (77.61%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 10/10 (LIMITADA) |
| Union SG vs Real Sociedad | Más de 1.5 goles (77.61%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 10/10 (LIMITADA) |
| Torreense vs Sunderland | Más de 1.5 goles (76.86%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/10 (BAJA) |
| Benfica vs Celtic | Más de 1.5 goles (75.09%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/10 (BAJA) |
| Bournemouth vs Sturm Graz | Más de 1.5 goles (74.48%) | No verificada | NO BET: ningún mercado calculado alcanza 75% | 10/10 (LIMITADA) |
| Celta Vigo vs Juventus | Menos de 3.5 goles (76.06%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 10/10 (LIMITADA) |
| Dinamo Zagreb vs Anderlecht | Menos de 3.5 goles (74.47%) | No verificada | NO BET: ningún mercado calculado alcanza 75% | 1/1 (BAJA) |
| Ferencváros vs Viktoria Plzeň | Más de 1.5 goles (79.48%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/1 (BAJA) |
| Hoffenheim vs Beşiktaş | Más de 1.5 goles (78.73%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/10 (BAJA) |
| Jagiellonia vs Ararat-Armenia | Más de 1.5 goles (80.96%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/1 (BAJA) |
| Marseille vs Olympiacos | Más de 1.5 goles (80.96%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/1 (BAJA) |
| NEC Nijmegen vs Levski Sofia | Más de 1.5 goles (75.86%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 10/1 (BAJA) |
| Rennes vs OFI Crete | Menos de 3.5 goles (76.61%) | No verificada | PROVISIONAL: falta cuota verificable para EV | 1/1 (BAJA) |

## Combinada de dos selecciones
**Lech Poznań–Leverkusen: Más de 1.5 goles + Sparta Praha–Lillestrøm: Más de 1.5 goles.**

- Probabilidad conjunta aproximada, suponiendo independencia: **67.67%**, superior al umbral del 65%.
- Cuota combinada: **no verificada**. No se multiplica ni se presenta como precio real de Betano sin cuotas confirmadas para ambas selecciones.
- Decisión: **no emitir apuesta combinada todavía**. La probabilidad por sí sola no basta para calcular valor esperado ni justificar una apuesta.

## Lectura de resultados
- La simulación base usa un modelo Poisson exploratorio y no validado específicamente para la Europa League. El historial es desigual; en varios partidos solo se identificó un juego por equipo. Por ello, los porcentajes son orientativos y no prueban una ventaja real.
- Para Sparta–Lillestrøm, el cálculo con la cuota listada es: probabilidad **80.96%**, cuota 1.18 y EV aproximado **-4.47%**. El EV aritmético es negativo, por lo que corresponde **NO BET**.
- En los mercados sin cuota verificada, se presenta el pronóstico y su probabilidad, pero no se finge que se calculó EV. Esto no es declarar todos los partidos insuficientes: es distinguir la evaluación probabilística de la económica.

## Fuentes
- Calendario oficial UEFA: https://www.uefa.com/uefaeuropaleague/news/02a8-2174cafa5bb6-82bbc20c9b92-1000--2026-27-europa-league-all-the-league-phase-fixtures-and-re/
- Referencia de cuotas para Sparta Praha–Lillestrøm: https://scorebob.com/en/match/1636276/sparta-praha-vs-lillestrom
- Probabilidades e historial calculados por la rama exploratoria del proyecto: https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/data/simulacion/simulacion_europa_league_2026-10-15.json
