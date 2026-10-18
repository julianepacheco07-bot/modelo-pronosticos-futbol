# Revisión postpartido del cupón — 18 de octubre de 2026

Zona horaria: America/Bogota. Esta es una revisión de un cupón concreto, no un backtest ni una validación de rentabilidad.

## Liquidación por selección

| Partido | Selección | Cuota registrada en conversación | Marcador | Estado |
|---|---|---:|---:|---|
| Groningen–Ajax | Ajax o empate + más de 1,5 goles | 1,47 | 2-5, según revisión previa; verificación independiente pendiente | Ganada según el marcador anotado |
| Molde–IK Start | Molde gana o lidera por 2 goles | 1,34 | 6-1, comunicado por el usuario | Ganada |
| Sandefjord–Lillestrøm | Más de 1,5 goles | 1,17 | 0-2, según revisión previa | Ganada; fuente independiente pendiente en este registro |
| Lorient–Mónaco | Mónaco o empate (X2) | 1,31 | 1-0, según revisión previa | Perdida |
| Nottingham Forest–Arsenal | Arsenal gana o lidera por 2 goles | 1,62 | 0-1, según revisión previa | Ganada; fuente independiente pendiente en este registro |

**Balance provisional:** 4/5 selecciones favorables (80 %), sujeto a verificar independientemente los resultados que en esta tabla se identifican como pendientes. Si las cinco eran parte de una sola combinada, el cupón completo pierde por Lorient–Mónaco.

**Producto teórico de cuotas:** 1,47 × 1,34 × 1,17 × 1,31 × 1,62 ≈ 4,89. No se ha confirmado que este fuera el precio final de Betano ni que las cuotas fueran capturadas con sello de tiempo verificable antes del inicio.

## Qué aprendimos y qué cambia

1. Separar siempre tres cosas: resultado de cada selección, liquidación del cupón completo y rentabilidad simulada.
2. Para «ganar o liderar por 2 goles», registrar si el equipo alcanzó una ventaja de al menos dos goles en cualquier momento, además del marcador final. La regla de liquidación se basa en lo comunicado por el usuario para Betano Colombia; la liquidación oficial de la casa debe conservarse si se dispone de ella.
3. No ajustar coeficientes ni calibrar probabilidades con cinco selecciones. Esta muestra es demasiado pequeña y sesgada para sacar conclusiones de calibración.
4. No calcular Brier, log loss, EV retrospectivo ni ROI de este cupón: faltan probabilidades prepartido congeladas, evidencia completa de las cuotas prepartido y confirmación del stake.
5. Distinguir procedencia: Molde–Start 6-1 fue comunicado directamente por el usuario; otros marcadores y cuotas anotados aquí no tienen todos verificación independiente ni hora de captura demostrada.
6. En futuras jornadas, guardar antes del partido la probabilidad de cada selección, cuota, fuente, hora de captura, regla de liquidación, versión del modelo y stake virtual; después añadir resultado y liquidación sin modificar el pronóstico original.

## Decisión

No se cambian parámetros del modelo por este cupón. Se refuerza el protocolo de auditoría postpartido y se mantiene «ganar o liderar por 2 goles» como mercado experimental, pendiente de validación fuera de muestra. El acierto puntual no prueba que el modelo esté calibrado ni que exista rentabilidad.
