# Resultado consolidado de auditoría — 15 de octubre de 2026

**Ejecución:** [Backtest OpenFootball #31](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38740882724)  
**Commit de código ejecutado:** `80884753d2a0b122195be69b85df1fdd7fa81a24`  
**Artefacto:** `backtest-openfootball-31` (ID `11975762515`)  
**Estado de CI:** éxito; pruebas unitarias, backtest y publicación del artefacto terminaron correctamente.  
**Cuotas históricas:** expresamente fuera del alcance y no requeridas para validar la capacidad predictiva.

## Resultado ejecutivo

Se ejecutó nuevamente el backtest con las 15 fuentes OpenFootball (cinco ligas europeas × tres temporadas). El artefacto confirma 5.256 filas de origen, 5.235 marcadores completos, cero duplicados exactos, cero conflictos de marcador, 4.883 partidos evaluables y 352 omitidos por historial previo insuficiente.

La ejecución es reproducible a nivel de código, datos capturados y artefacto. **Esto no cierra la discrepancia con los informes históricos anteriores ni demuestra que el modelo esté listo para apostar.** Las métricas de esta ejecución deben tratarse como una nueva línea base auditada; los antiguos resultados de 4.770 partidos y 52,935 % de exactitud no quedaron reconciliados partido por partido.

## Resultados de los ocho pasos

| Paso | Resultado de la auditoría | Estado |
|---|---|---|
| 1. Conciliar la base histórica | Se regeneró el inventario de las 15 fuentes: 5.256 filas; 5.235 válidas; 21 incompletas; 0 duplicados exactos; 0 conflictos. Los 352 partidos sin historial mínimo quedan identificados como omitidos. La diferencia de 113 partidos frente al informe antiguo de 4.770 **sigue sin reconciliarse** porque faltan los snapshots/predicciones originales comparables. | Parcial: nueva base verificada; histórico antiguo pendiente |
| 2. Reproducir el backtest | GitHub Actions ejecutó pruebas y backtest, generó el Excel con detalle por partido, métricas, fuentes y hashes. | Completado para esta versión |
| 3. Validación temporal independiente | El código usa partidos con fecha estrictamente anterior al objetivo y prueba temporadas posteriores a las de ajuste. Se ejecutó evaluación por temporadas 2024-25 y 2025-26. La independencia exacta respecto de los informes antiguos no puede probarse sin las predicciones originales. | Completado para la nueva línea base; reconciliación antigua pendiente |
| 4. Calibración | Se probó temperature scaling con temperaturas ajustadas solo sobre temporadas anteriores. El log loss mejora modestamente en ambos periodos de prueba para los tres modelos Poisson; no mejora para la línea base de frecuencia. | Completado exploratoriamente; mejora pequeña |
| 5. Comparación de modelos | Se compararon tres variantes Poisson y una línea base de frecuencia histórica, sobre las mismas 4.883 filas. Bootstrap pareado de 3.000 remuestras y bootstrap por bloques liga-temporada de 3.000 remuestras. | Completado; diferencias entre los dos modelos principales no concluyentes |
| 6. Robustez | Se calcularon métricas por las cinco ligas y tres temporadas, además de intervalos descriptivos. El ganador cambia por liga-temporada; solo hay 15 bloques liga-temporada y dos temporadas de prueba, por lo que los intervalos por bloques son orientativos. | Parcial; hace falta más historia congelada y más temporadas |
| 7. Validación por mercado | El backtest europeo de esta ejecución valida exclusivamente 1X2. Existe un backtest exploratorio sudamericano separado para Over 1.5, Under 3.5 y ambos marcan, pero no hay en este artefacto una comparación homogénea validada de todos los mercados. | Parcial; 1X2 ejecutado, otros mercados requieren auditoría independiente |
| 8. Reglas de decisión | Se conserva la separación entre probabilidad deportiva y decisión económica. La ausencia de cuotas históricas no bloquea el backtest. EV/ROI solo se medirán prospectivamente con cuotas reales registradas desde el inicio de la simulación y después de liquidar selecciones. No forzar NO BET: usar APUESTA CANDIDATA, NO BET o ANÁLISIS INSUFICIENTE según evidencia y precio actual verificado. | Regla documentada; ROI prospectivo pendiente de muestra liquidada |

## Métricas globales regeneradas

| Modelo | N | Exactitud 1X2 | Brier multiclase | Log loss |
|---|---:|---:|---:|---:|
| Poisson con multiplicadores 1,10/0,90 | 4.883 | 48,80 % | 0,618848 | 1,030323 |
| Poisson neutral 1,00/1,00 | 4.883 | 47,96 % | 0,627266 | 1,042172 |
| Poisson ajustado por localía/visita | 4.883 | 48,78 % | 0,619985 | 1,033297 |
| Frecuencia histórica suavizada | 4.883 | 42,92 % | 0,652465 | 1,077885 |

En estas métricas, menor Brier y menor log loss son mejores. Los multiplicadores 1,10/0,90 obtienen el mejor agregado, pero superan por poco al modelo ajustado por localía/visita.

### Validación por temporada

| Temporada | N | Multiplicadores: exactitud | Brier | Log loss |
|---|---:|---:|---:|---:|
| 2023-24 | 1.510 | 50,33 % | 0,61053 | 1,01822 |
| 2024-25 | 1.665 | 48,17 % | 0,61883 | 1,02982 |
| 2025-26 | 1.708 | 48,07 % | 0,62622 | 1,04151 |

La degradación de Brier/log loss entre las temporadas 2023-24 y 2025-26 es una señal de que el rendimiento no es estable y debe seguirse investigando.

## Calibración temporal

El ajuste se realizó con temporadas anteriores, sin usar la temporada de prueba para escoger la temperatura:

| Modelo | Prueba | Temperatura elegida | Log loss original | Log loss calibrado |
|---|---|---:|---:|---:|
| Multiplicadores 1,10/0,90 | 2024-25 | 1,075 | 1,029821 | 1,028743 |
| Multiplicadores 1,10/0,90 | 2025-26 | 1,100 | 1,041514 | 1,039868 |
| Neutral 1,00/1,00 | 2024-25 | 1,125 | 1,036672 | 1,035381 |
| Neutral 1,00/1,00 | 2025-26 | 1,125 | 1,056582 | 1,053780 |
| Ajustado por localía/visita | 2024-25 | 1,150 | 1,034782 | 1,032750 |
| Ajustado por localía/visita | 2025-26 | 1,150 | 1,039495 | 1,037448 |

La mejora es pequeña; no debe describirse como una calibración definitiva ni como evidencia de ventaja de apuestas. La línea base de frecuencia no mejoró con el ajuste.

## Comparaciones pareadas

Sobre las mismas 4.883 predicciones, el bootstrap por partido (3.000 remuestras) muestra:

- Multiplicadores frente a frecuencia histórica: +5,88 puntos porcentuales de exactitud; diferencia de Brier −0,03362 y de log loss −0,04756, favoreciendo los multiplicadores.
- Multiplicadores frente al modelo neutral: Brier y log loss favorecen a los multiplicadores; la diferencia de exactitud no es concluyente.
- Multiplicadores frente al ajuste localía/visita: diferencias no concluyentes en exactitud, Brier y log loss.

El bootstrap por bloques liga-temporada también se calculó, pero tiene solo 15 bloques y dos temporadas de prueba; sus intervalos son orientativos y no una prueba definitiva de generalización.

## Corrección técnica aplicada

En `src/backtest_openfootball.py` se añadió un control de cobertura completa: la ejecución ahora falla de forma explícita si falta cualquiera de las 15 combinaciones liga-temporada o si hay errores de recuperación, en lugar de producir silenciosamente un resultado parcial. El manifiesto distingue entre archivos descargados en esa ejecución y archivos reutilizados desde caché local. Esta ejecución registró 15/15 como `downloaded_now`, cero errores y cobertura completa.

También se actualizó `docs/METODOLOGIA.md` para dejar inequívoco que las cuotas históricas no se buscan ni reconstruyen y no son requisito del backtest predictivo. EV/ROI son un seguimiento prospectivo separado.

## Dictamen final

1. **Backtest técnico:** ejecutado correctamente; pruebas automáticas y artefacto publicados.
2. **Capacidad predictiva 1X2:** medible y superior a la línea base de frecuencia en esta muestra, pero con exactitud agregada inferior al 50 % y resultados que cambian por temporada y liga.
3. **Calibración:** mejora pequeña en log loss para los tres modelos Poisson; no basta para declarar calibración satisfactoria.
4. **Histórico anterior:** discrepancia de 113 partidos y de métricas aún no reconciliada; no atribuir una causa sin los archivos y predicciones originales.
5. **Mercados distintos de 1X2:** necesitan evaluación independiente, sin mezclar resultados de distintos conjuntos o metodologías.
6. **Rentabilidad:** no evaluada en este backtest y no bloqueada por la ausencia de cuotas históricas. Se iniciará con las cuotas prospectivas registradas y resultados liquidados.
7. **Decisión operativa:** esta versión sirve como línea base experimental; no debe presentarse como modelo validado para apostar ni usarse para afirmar rentabilidad.

## Artefactos de la ejecución

- [Workflow de GitHub Actions #31](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/actions/runs/38740882724)
- [Script de backtest actualizado](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/src/backtest_openfootball.py)
- [Metodología actualizada](https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/docs/METODOLOGIA.md)
