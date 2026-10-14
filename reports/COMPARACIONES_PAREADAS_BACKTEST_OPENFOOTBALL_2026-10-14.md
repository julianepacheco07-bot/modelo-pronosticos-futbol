# Comparaciones pareadas del backtest OpenFootball

Fecha de implementación: 2026-10-14.

## Qué se añadió

El script `src/backtest_openfootball.py` calcula una hoja `Comparaciones_pareadas` en el libro de resultados. Compara cuatro pares predefinidos de modelos mediante diferencias pareadas por partido para exactitud, Brier y LogLoss. Se mantienen las mismas filas al comparar A y B; el signo reportado es siempre métrica de A menos métrica de B.

- 3.000 remuestras bootstrap por comparación.
- Semilla fija: `20261014`.
- Intervalo percentil del 95 %.
- La hoja indica el sentido de la diferencia, el número de partidos, la semilla y una interpretación cautelosa del intervalo.
- Prueba automatizada de reproducibilidad, tamaño de salida y diferencia de exactitud en datos sintéticos.

## Cómo interpretar

- Para **Exactitud**, un valor positivo favorece A; uno negativo favorece B.
- Para **Brier** y **LogLoss**, valores menores son mejores: una diferencia positiva favorece B y una negativa favorece A.
- Si el intervalo de confianza incluye cero, el resultado se etiqueta como no concluyente bajo este procedimiento; no debe leerse como prueba de equivalencia.
- El bootstrap actual remuestrea partidos individuales. No modela completamente la dependencia temporal, las jornadas, los equipos repetidos ni los cambios de distribución entre temporadas. Es una incertidumbre descriptiva, no una garantía de generalización.

## Límites de la evidencia

Estas métricas evalúan resultados probabilísticos históricos, no rentabilidad de apuestas. No se calcula EV ni ROI porque no se dispone de cuotas históricas verificadas y sincronizadas con cada partido. La precisión de clasificación tampoco basta para concluir que un modelo es rentable.

El backtest aplica el corte temporal definido por el protocolo: solo usa partidos con fecha estrictamente anterior al encuentro evaluado. Los partidos sin historial mínimo suficiente se omiten, y deben revisarse en la hoja `Omitidos`.

Los resultados numéricos válidos para cada ejecución son los del artefacto generado por GitHub Actions junto con su manifiesto de fuentes y hashes. Los datos upstream pueden cambiar; no se deben presentar cifras de una ejecución anterior como si fueran las de la más reciente.


## Resultado verificado de la ejecución 14

Ejecución: [GitHub Actions #14](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38583387445). Estado observado: **success**. El paso de pruebas unitarias y el paso del backtest terminaron correctamente. El artefacto publicado es `backtest-openfootball-14` (ID `11903633239`); se descargó y se verificó que el Excel contiene la hoja `Comparaciones_pareadas` con 12 filas (4 pares × 3 métricas).

| Comparación A − B | Métrica | Diferencia | IC 95 % | Lectura |
|---|---|---:|---:|---|
| multipliers − baseline_frequency | Exactitud | +0.058775 | [0.044230, 0.073316] | A mejor |
| multipliers − baseline_frequency | Brier | −0.033617 | [−0.040365, −0.026922] | A mejor |
| multipliers − baseline_frequency | LogLoss | −0.047561 | [−0.057052, −0.037563] | A mejor |
| venue_adjusted − baseline_frequency | Exactitud | +0.058571 | [0.044030, 0.072087] | A mejor |
| venue_adjusted − baseline_frequency | Brier | −0.032480 | [−0.039095, −0.025589] | A mejor |
| venue_adjusted − baseline_frequency | LogLoss | −0.044588 | [−0.054391, −0.034593] | A mejor |
| multipliers − venue_adjusted | Exactitud | +0.000205 | [−0.011468, 0.012083] | No concluyente |
| multipliers − venue_adjusted | Brier | −0.001137 | [−0.006970, 0.004549] | No concluyente |
| multipliers − venue_adjusted | LogLoss | −0.002974 | [−0.011216, 0.005455] | No concluyente |
| multipliers − neutral | Exactitud | +0.008396 | [−0.000819, 0.017612] | No concluyente |
| multipliers − neutral | Brier | −0.008418 | [−0.011332, −0.005671] | A mejor |
| multipliers − neutral | LogLoss | −0.011849 | [−0.015797, −0.007952] | A mejor |

En esta ejecución, el backtest incluyó 4.883 partidos evaluables, con 352 omitidos por historial previo insuficiente. La exactitud global fue 48.80 % para `multipliers_1.10_0.90`, 48.78 % para `venue_adjusted`, 47.96 % para `neutral_1.00_1.00` y 42.92 % para `baseline_frequency`. Estos porcentajes no son tasas de acierto de apuestas seleccionadas a cuotas de mercado y no demuestran rentabilidad. **No se calculó EV ni ROI**, por falta de cuotas históricas verificadas.

## Reproducción

Ejecutar el flujo **Backtest OpenFootball** en GitHub Actions. Verificar que las pruebas pasan y que el Excel descargado contiene `Comparaciones_pareadas`. La semilla y el número de remuestras se registran en cada fila de esa hoja.
