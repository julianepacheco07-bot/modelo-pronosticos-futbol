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

## Reproducción

Ejecutar el flujo **Backtest OpenFootball** en GitHub Actions. Verificar que las pruebas pasan y que el Excel descargado contiene `Comparaciones_pareadas`. La semilla y el número de remuestras se registran en cada fila de esa hoja.
