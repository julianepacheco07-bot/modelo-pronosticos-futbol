# Inferencia estadística del backtest — 2026-10-18

Ejecución de GitHub Actions: https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/39139122612  
Commit evaluado: `c8e0870885039114efeee8630ff13f9a1ae6dd9e`  
Muestra: 4.883 partidos, 5 ligas, temporadas 2023-24 a 2025-26. Bootstrap pareado de 2.000 remuestreos. Diferencias definidas como Poisson menos baseline; valores negativos favorecen Poisson.

| Mercado | Delta Brier | IC 95% | Delta log loss | IC 95% | Conclusión |
|---|---:|---|---:|---|---|
| 1X2 | -0,032464 | [-0,037803; -0,027081] | -0,044612 | [-0,051966; -0,037185] | Intervalos completamente negativos |
| Over 1.5 | -0,000137 | [-0,001418; 0,001103] | -0,000757 | [-0,004291; 0,002716] | No concluyente |
| Under 3.5 | -0,001253 | [-0,002849; 0,000469] | -0,003094 | [-0,006914; 0,000997] | No concluyente |
| Ambos marcan sí | -0,000263 | [-0,001751; 0,001253] | -0,000460 | [-0,003514; 0,002706] | No concluyente |

## Interpretación
- Para 1X2, el bootstrap por partido respalda que el Poisson tiene menor pérdida que la referencia histórica dentro de esta muestra.
- En Over 1.5, Under 3.5 y Ambos marcan, los intervalos incluyen cero. No hay evidencia suficiente de mejora consistente frente a la referencia.
- Los intervalos son un bootstrap sencillo por partido; no corrigen completamente dependencia temporal, cambios de temporada o diferencias entre ligas. Debe tratarse como evidencia preliminar.
- Esto no demuestra valor económico: no se usaron cuotas ni se calculó ROI.

## Comparación con cuotas de mercado
No hay en el conjunto evaluado cuotas históricas prepartido verificadas y sincronizadas para las 4.883 observaciones, por lo que no es válido reconstruirlas ni afirmar una comparación histórica con el mercado.

A partir de ahora se inicia una comparación prospectiva: antes de cada partido se guardarán mercado, cuota decimal, casa/fuente, hora de captura, probabilidad Poisson, probabilidad implícita bruta y probabilidad sin margen cuando estén disponibles todas las cuotas complementarias del mismo mercado. Después del partido se añadirá el resultado. Las capturas incompletas se etiquetarán como pendientes, no como ventaja ni como fallo.

## Decisión
Mantener Poisson como modelo experimental para 1X2; no declarar validados los mercados de goles. El mercado «ganar o alcanzar ventaja de dos goles» se registra únicamente desde ahora, sin backfill histórico.
