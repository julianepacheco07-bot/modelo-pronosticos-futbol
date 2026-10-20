# Plan de recalibración — modelo de goles y mercados

**Estado: recalibración pendiente; no se cambian parámetros hasta tener predicciones históricas reproducibles.**  
**Fecha de decisión:** 19 de octubre de 2026.

## Decisión

Sí hace falta una recalibración, pero no es válido ajustar el modelo a partir de un único partido (Deportivo Pasto 0-1 Alianza FC). Ese resultado se registra como evaluación, no como dato para optimizar parámetros. Las probabilidades comunicadas para las combinadas (43,0% y 53,8%) procedieron de un Poisson simplificado no validado para Liga BetPlay y quedan clasificadas como exploratorias, no como pronósticos oficiales.

## Diagnóstico de la línea base existente

El informe `data/evaluacion/backtest_temporal_2023_2026.md` documenta una evaluación temporal de cinco ligas europeas. Sus promedios de probabilidad para Over 1.5 y Under 3.5 están próximos a las frecuencias observadas agregadas, pero esas medias no prueban calibración por intervalos ni capacidad para Liga BetPlay. El backtest no contiene un conjunto de predicciones por partido que permita recalibrar probabilidades después del hecho.

**No trasladar automáticamente los parámetros europeos a Colombia.** Los mercados de goles requieren una evaluación específica por competición y temporada.

## Protocolo de recalibración que se debe ejecutar

1. **Datos:** construir una tabla de resultados de Liga BetPlay con fecha, temporada, equipos y goles finales, y documentar la fuente, licencia, cobertura y correcciones. No usar datos en vivo ni variables posteriores al inicio.
2. **Variables prepartido:** para cada partido, calcular únicamente con encuentros anteriores: forma reciente con decaimiento temporal, goles a favor/contra separados por localía, fuerza del rival y promedio de la competición. Exigir un mínimo de historial y aplicar suavizado para muestras pequeñas.
3. **Corte temporal:** rolling-origin por fecha; nunca dividir aleatoriamente. Congelar cada predicción antes de incorporar el resultado de ese partido.
4. **Candidatos comparables:** (A) Poisson simple actual; (B) Poisson con ataque/defensa por equipo y localía; (C) el modelo B con suavizado/decay seleccionado solo dentro de validación temporal. No elegir un modelo solo porque predice mejor un partido individual.
5. **Calibración:** evaluar 1X2 con Brier multiclase y log loss; mercados Over 1.5, Under 3.5 y BTTS con Brier y log loss. Incluir diagramas/tablas de calibración por bandas, tamaño de muestra e intervalos bootstrap por partido/fecha.
6. **Comparación:** contrastar con una línea base de frecuencias históricas de la competición y con el modelo Poisson actual. Reportar diferencias pareadas e intervalos de confianza; si la mejora no es clara, conservar el modelo simple y declarar incertidumbre.
7. **Prueba final:** reservar la temporada más reciente como test final sin usarla para elegir parámetros. No cambiar el modelo tras observar sus resultados.
8. **Combinadas:** calcular la probabilidad conjunta desde la distribución de marcadores (o un modelo conjunto validado), no multiplicar marginales por defecto. Evaluar calibración de la probabilidad conjunta por rangos. La cuota solo se usa si fue capturada y registrada antes del inicio.
9. **Despliegue:** solo sustituir el modelo activo si mejora frente a la línea base en métricas fuera de muestra y la mejora es estable. Guardar versión, configuración, hashes de datos y reporte reproducible.

## Limitación operativa de esta actualización

En esta sesión se inspeccionaron los archivos y métricas existentes del repositorio, pero no se pudo clonar ni ejecutar el código en un entorno con acceso de red al repositorio. Tampoco se recuperó todavía un archivo histórico de Liga BetPlay con cobertura y licencia verificadas para ejecutar el protocolo. Por eso **no se afirma que la recalibración numérica se haya ejecutado** y no se han cambiado parámetros del modelo.

## Fuente de datos a evaluar (no aprobada automáticamente)

- Footiqo ofrece vistas descargables de resultados históricos de Colombia Primera A: https://footiqo.com/es/base-de-datos/ligas/colombia-primera-a/
- SoccerPunter publica archivos de resultados por temporada: https://www.soccerpunter.com/stats/353/Colombia

Antes de incorporarlos, verificar cobertura completa, definición de temporada, consistencia de nombres y condiciones de reutilización. No usar cuotas históricas para calcular ROI ni importar cuotas anteriores al inicio del registro prospectivo.

## Criterio de cierre

La recalibración solo puede marcarse como completada cuando el script genera predicciones fuera de muestra, métricas y artefactos que otro usuario pueda reproducir desde el repositorio. Hasta entonces el estado del modelo para Liga BetPlay es **experimental / calibración insuficiente**.
