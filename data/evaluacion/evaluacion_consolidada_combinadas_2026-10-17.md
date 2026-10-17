# Evaluación consolidada de combinadas — 17/10/2026

## Criterio de auditoría

Se comparan las selecciones capturadas en los cupones con los marcadores finales consultados el 17/10/2026. Los marcadores se contrastaron con listados de resultados publicados por Goal.com, Depor y otros medios deportivos. Las cuotas se consideran las que aparecían en las capturas del usuario; no se afirma que sean cuotas de cierre ni que se hayan verificado directamente en Betano. No se calculan rentabilidad ni valor esperado sin stake, pago liquidado y probabilidades previas guardadas.

## Combinada 1 — cuota total mostrada: 3,12

| Partido | Selección | Cuota individual capturada | Marcador final | Liquidación |
|---|---|---:|---:|---|
| Everton vs Chelsea | Chelsea o empate | 1,39 | 0–2 | Acierto |
| Espanyol vs Atlético de Madrid | Atlético o empate + más de 1,5 goles | 1,50 | 0–1 | Fallo: se cumplió Atlético o empate, falló más de 1,5 goles |
| Ham-Kam vs Bodø/Glimt | Gana Bodø/Glimt | 1,24 | 0–2 | Acierto |
| Venezia vs Napoli | Napoli o empate | 1,21 | 1–0 | Fallo |

**Resultado:** 2 de 4 selecciones acertadas; la combinada completa perdió. La condición conjunta de Espanyol–Atlético debe evaluarse como una selección compuesta: no basta con acertar una de sus dos partes.

## Combinada 2 — cuota total mostrada: 4,96

| Partido | Selección | Cuota individual capturada | Marcador final | Liquidación |
|---|---|---:|---:|---|
| Union Berlin vs Borussia Dortmund | Más de 2,5 goles | 1,55 | 0–0 | Fallo |
| Schalke 04 vs Mainz 05 | Schalke o empate | 1,60 | 0–1 | Fallo |
| Manchester City vs Ipswich | Mercado de victoria/margen de goles según la captura | 1,25 | 3–2 | Pendiente de liquidación exacta: si era victoria simple de City, acierto; si exigía ganar por 2 o más, fallo |
| Hamburg vs Stuttgart | Victoria de Stuttgart | 1,60 | 1–0 | Fallo |

**Resultado:** tres selecciones fallidas confirmadas y una pendiente de verificar según la regla exacta del mercado del Manchester City. La selección de más de 2,5 goles en Union–Dortmund fue un fallo: el marcador final fue 0–0. Esto corrige la anotación preliminar anterior que la había tratado como acierto basándose en un reporte no confirmado.

## Balance conjunto

- Combinada 1: 2/4 selecciones acertadas; boleto perdido.
- Combinada 2: 0/3 selecciones con liquidación confirmada; una selección pendiente por ambigüedad del mercado; boleto perdido en cualquier caso porque ya fallaron otras tres selecciones.
- No se infiere rentabilidad a partir de los aciertos individuales. Para calcular ROI hacen falta importe apostado y pago final de cada boleto.
- No se calcula Brier ni log loss porque no se guardaron probabilidades prepartido calibradas para cada resultado evaluado.
- No se reajustan probabilidades retroactivamente ni se afirma que el modelo haya sido validado por dos cupones.

## Acciones metodológicas

1. Guardar antes del inicio de cada partido la probabilidad del evento, la cuota capturada, la hora y fuente de captura, y la regla de liquidación exacta.
2. Para mercados combinados dentro de un partido, guardar las probabilidades de cada componente y la probabilidad conjunta estimada; no asumir independencia sin justificación.
3. Registrar tanto aciertos como fallos, incluyendo las selecciones que se recomendaron retirar o que se identificaron como riesgosas.
4. Mantener separado el resultado del cupón de la evaluación predictiva: un boleto perdido no mide por sí solo la calibración, y acertar una selección tampoco demuestra ventaja estadística.
5. Revisar la transcripción del mercado Manchester City–Ipswich desde la captura original antes de registrar su liquidación definitiva.

## Fuentes de marcadores consultadas

- Goal.com, resultados del 17/10/2026: https://www.goal.com/en/results/2026-10-17
- Depor, resultados de fútbol del 17/10/2026: https://depor.com/resultados/
- The Guardian, cobertura Everton–Chelsea y Manchester City–Ipswich del 17/10/2026: https://www.theguardian.com/football/live/2026/oct/17/manchester-city-v-ipswich-brentford-v-liverpool-and-more-football-clockwatch-live

Los resultados consultados son referencias externas para los marcadores; las cuotas y el contenido exacto de los cupones provienen de las capturas del usuario.
