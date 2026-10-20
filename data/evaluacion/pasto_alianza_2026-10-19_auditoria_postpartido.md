# Auditoría postpartido: Deportivo Pasto 0-1 Alianza FC

- **Fecha local:** 19 de octubre de 2026, Liga BetPlay II, jornada 15.
- **Marcador:** Deportivo Pasto 0-1 Alianza FC. El resultado y el goleador (Israel Alba, 38') aparecen en el directo de Caracol Radio.
- **Estado de la predicción:** ambas combinadas propuestas se liquidan como perdidas porque el componente común «Pasto o empate (1X)» falló.
- **Cuotas observadas aportadas por el usuario antes del partido:** 1X + más de 1.5 goles @ 1.62; 1X + menos de 3.5 goles @ 1.47.
- **Estimaciones exploratorias comunicadas antes del partido:** 43,0% y 53,8%, respectivamente, mediante Poisson simplificado con tasas aproximadas λ(Pasto)=1,15 y λ(Alianza)=1,09.
- **Advertencia metodológica:** estas dos cifras no deben considerarse predicciones oficiales reproducibles del modelo completo ni probabilidades calibradas. No se debe actualizar el modelo con el resultado aislado ni reconstruir cuotas históricas.

## Estadísticas del partido disponibles en fuentes públicas

### Caracol Radio
Página de estadísticas: https://caracol.com.co/resultados/futbol/colombia_ii/2026/directo/regular_a_15_6a2d5d4121fff87/estadisticas/

En el rastreo de la página, el partido estaba en el minuto 76 y mostraba:
- Marcador: Pasto 0-1 Alianza; gol de Israel Alba al 38'.
- Posesión: Pasto 70,8%; Alianza 29,2%.
- Disparos recibidos (etiqueta de la fuente): 5 y 8.
- Remates: la página presenta 3 y 2 en la categoría «fuera», 1 y 2 en «dentro», y 3 y 2 bloqueados; la extracción de texto no conserva de forma fiable la alineación visual por equipo, por lo que no se atribuyen aquí los subtotales a cada club.
- Amarillas: 0 y 1; rojas: 0 y 0.
- Faltas recibidas: 14 y 7; faltas cometidas: 9 y 15.
- Pérdidas de posesión: 116 y 82; recuperaciones: 34 y 31; fueras de juego: 1 y 0.
- **Importante:** esta captura indexada de estadísticas corresponde a un estado en directo (minuto 76), no se debe etiquetar como estadística final.

### Flashscore
Página de estadísticas: https://www.flashscore.com/match/football/alianza-GfFNymsk/dep-pasto-GdemgvJl/summary/stats/

El resultado de búsqueda de Flashscore seguía mostrando el encuentro como próximo y decía que las estadísticas estarían disponibles al comenzar; no se obtuvo de esta consulta un cuadro final fiable de estadísticas. No se inventan datos para completar el registro.

### Sofascore
Ficha del partido: https://www.sofascore.com/football/match/alianza-valledupar-fc-deportivo-pasto/nxcsZXbe

Sofascore identifica el encuentro de Liga DIMAYOR, Finalización, jornada 15, con inicio listado el 20 de octubre a las 01:05 UTC (equivalente a 19 de octubre a las 20:05 en Colombia). La ficha consultada no expuso estadísticas finales verificables en el contenido recuperado. No se atribuyen estadísticas de partido a Sofascore sin haberlas podido leer.

## Interpretación técnica

1. **Fallo del mercado compartido:** las dos combinadas fallaron por el 1X, mientras que el under 3.5 sí se habría cumplido como selección individual con marcador 0-1.
2. **No sobreajustar:** una derrota de una selección no prueba que su probabilidad prepartido estuviera mal calibrada. Hace falta una muestra de predicciones congeladas y resultados para evaluar calibración, Brier Score y Log Loss.
3. **Problema previo detectado:** las tasas λ=1,15 y 1,09 se presentaron como aproximación sencilla; no se documentó una ejecución reproducible con datos completos de Liga BetPlay, ajustes por localía, fuerza de rivales y forma ponderada. Por ello, las probabilidades 43,0% y 53,8% deben conservarse solo como estimaciones exploratorias, no como salidas validadas.
4. **Acción necesaria para una auditoría completa:** ejecutar el pipeline del repositorio en una muestra histórica de Liga BetPlay con cortes temporales estrictos, guardar predicciones fuera de muestra antes de cada partido y evaluar calibración por mercado. No se declara aquí que esa ejecución se haya realizado.
5. **Datos de cuotas:** las cuotas Betano se registran como aportadas por el usuario; faltan timestamp verificable/captura archivada y commit exacto del modelo usado. No calcular ROI a partir de esta única selección.

## Fuentes
- Caracol Radio, directo y estadísticas (estado consultado cerca del minuto 76): https://caracol.com.co/resultados/futbol/colombia_ii/2026/directo/regular_a_15_6a2d5d4121fff87/estadisticas/
- Flashscore, ficha estadística: https://www.flashscore.com/match/football/alianza-GfFNymsk/dep-pasto-GdemgvJl/summary/stats/
- Sofascore, ficha del partido: https://www.sofascore.com/football/match/alianza-valledupar-fc-deportivo-pasto/nxcsZXbe


## Ampliación con datos de la ficha de partido (consulta posterior)

Una ficha estadística indexada de AS/Caracol, consultada el 20 de octubre de 2026, publica datos de temporada previos/alrededor del partido (no son estadísticas del encuentro en sí):
- Goles por partido: Pasto 0,8 (9 goles); Alianza 1,1 (14 goles).
- Goles encajados por partido: Pasto 1,5 (18); Alianza 2,0 (26).
- Disparos recibidos por partido: Pasto 12,8 (153); Alianza 11,9 (155).
- Pases por partido: Pasto 425,8 (5.110); Alianza 336,2 (4.370).
Fuente: https://colombia.as.com/resultados/futbol/colombia_ii/2026/directo/regular_a_15_6a2d5d4121fff87/

Estos totales de temporada sugieren que Alianza concedía más goles por partido y Pasto anotaba poco; sirven como contexto, pero no reemplazan la muestra separada local/visitante ni se deben usar como si fueran datos exclusivamente prepartido sin comprobar el corte temporal exacto.

## Estado de ejecución del modelo

En esta actualización se consultaron los archivos del repositorio y las páginas públicas disponibles, pero **no se ejecutó de nuevo el backtest completo** ni se generaron métricas nuevas. El backtest documentado en `backtest_temporal_2023_2026.md` cubre cinco ligas europeas, no la Liga BetPlay colombiana. Por ello no hay base para afirmar que el pipeline existente validó este partido o que ya esté calibrado para Colombia.

Siguiente tarea técnica: incorporar una fuente histórica verificable para Liga BetPlay, construir variables estrictamente prepartido con corte temporal, ejecutar validación rolling-origin por temporada y reportar Brier/Log Loss para 1X2 y mercados de goles. Las cuotas de Betano de este encuentro permanecen como datos aportados por el usuario, no como captura archivada verificable.
