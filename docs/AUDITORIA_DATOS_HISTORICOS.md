# Auditoría inicial de archivos y datos históricos

**Fecha de revisión:** 2026-10-14  
**Repositorio:** `julianepacheco07-bot/modelo-pronosticos-futbol`  
**Estado:** auditoría documental inicial; no constituye una nueva ejecución independiente del backtest.

## 1. Archivos localizados en la biblioteca de trabajo

Se localizaron estos artefactos históricos fuera del repositorio GitHub, en la biblioteca de ChatGPT:

- `Backtest_Multitemporada_Modelo_Futbol_Resultados.xlsx`
- `Auditoria_Integral_Backtest_Futbol_Recalculado.xlsx`
- `Backtest_Estrictamente_Fuera_de_Muestra_2025_26.xlsx`
- `Validacion_Estricta_Fuera_de_Muestra_Futbol.xlsx`
- `Validacion_Temporal_y_Calibracion_Modelo_Futbol.xlsx`
- `Auditoria_Tecnica_Backtest_Modelo_recalculado_sin_cuotas.xlsx`
- `Auditoria_Tecnica_Backtest_Historial_corregido_y_validacion_modelo.xlsx`
- `Auditoria_Tecnica_Backtest_Auditoria_integral_cobertura_duplicados.xlsx`
- `Prototipo_Modelo_Futbol_Multiliga.xlsx`
- `Muestra_Historica_Multiliga.csv`
- `ejecutar_backtest_multitemporada.py`
- `crear_base_openfootball.py`

La presencia de estos archivos en la biblioteca no significa que estén versionados en GitHub. En la revisión del repositorio, solo se había confirmado el README y la metodología; los datos fuente y el código no estaban todavía incorporados allí.

## 2. Qué contienen los archivos examinados

### Muestra histórica
`Muestra_Historica_Multiliga.csv` contiene 73 partidos de muestra, correspondientes a cinco ligas en 2024/25. El propio archivo indica que los registros fueron transcritos y que la verificación independiente partido a partido está pendiente. No es suficiente como base completa para el backtest multitemporada.

### Reporte multitemporada previo
`Backtest_Multitemporada_Modelo_Futbol_Resultados.xlsx` reporta 4.770 partidos evaluados y métricas agregadas. Es un resumen con hojas de resultados y metodología; no contiene por sí solo la base detallada necesaria para regenerar cada predicción.

### Auditoría integral previa
`Auditoria_Integral_Backtest_Futbol_Recalculado.xlsx` reporta:
- 5.235 partidos con marcador final usable en 15 archivos (5 ligas × 3 temporadas).
- 4.883 partidos evaluables y 352 omitidos por historial previo insuficiente.
- 3.175 partidos de entrenamiento (2023-24 y 2024-25) y 1.708 partidos de prueba (2025-26).
- Ningún ROI ni valor esperado calculado, por ausencia de cuotas históricas prepartido.

Estos son valores consignados en un reporte previo, no cifras regeneradas de forma independiente durante esta auditoría.

## 3. Discrepancia de conteos pendiente de resolver

Los reportes previos discrepan en 113 partidos:
- Reporte multitemporada: 4.770 evaluables; 1.595 de la temporada 2025-26.
- Auditoría integral: 4.883 evaluables; 1.708 de la temporada 2025-26.

La auditoría integral identifica la diferencia, pero los archivos fuente completos y el detalle de predicciones que permitirían reproducir y explicar las 113 filas no se encuentran actualmente en el repositorio GitHub. Por tanto, no se debe tratar el conteo de 4.883 como definitivamente reconciliado hasta repetir la importación, identificar duplicados y comparar los partidos por una clave estable.

## 4. Hallazgos técnicos del script localizado

El archivo `ejecutar_backtest_multitemporada.py` documenta una descarga de CSV de DataHub para cinco ligas y tres temporadas. En su versión localizada se identifican controles pendientes antes de considerarlo reproducible:

1. El bloque de formato de Excel usa `Font` y `PatternFill`, pero no aparecen importados en el código inspeccionado; tal como está, la generación final del libro puede fallar con `NameError`.
2. Los duplicados se identifican y exportan, pero no se eliminan ni se bloquea el cálculo cuando existen. Así, un duplicado podría contarse más de una vez en métricas.
3. La normalización de fechas intenta dos interpretaciones, pero no registra una resolución explícita de fechas ambiguas. Se debe contrastar la interpretación con la fuente y el formato de cada archivo.
4. El código recupera datos de la web si los CSV no existen localmente. Para reproducibilidad, deben conservarse los archivos fuente usados, sus URL, fecha de descarga y hashes; no depender de que el contenido remoto siga igual.
5. El código construye historial por nombre exacto de equipo. Alias o cambios de nombre no se unifican automáticamente y pueden reducir el historial disponible o dividirlo.
6. La ejecución debe probarse de extremo a extremo en un entorno limpio y dejar guardados el manifiesto de fuentes, los datos importados, las exclusiones, los duplicados y el detalle de predicciones.

Estos puntos son hallazgos de revisión estática del script; todavía no se ha ejecutado una nueva descarga y un backtest independiente desde cero.

## 5. Conclusión provisional

Hay reportes útiles, un prototipo, una muestra parcial y un script candidato. Sin embargo, **no se ha demostrado todavía que el backtest completo pueda regenerarse de forma independiente desde los datos fuente exactos**. El repositorio GitHub tampoco contiene aún esos datos ni el código de ejecución.

No se publicará ninguna afirmación de rentabilidad: no hay cuotas históricas prepartido verificadas ni cálculo de EV/ROI en los artefactos examinados.

## 6. Acciones siguientes

- [ ] Recuperar o volver a descargar las 15 fuentes CSV exactas y guardarlas con URL, fecha y hash.
- [ ] Corregir el script (imports, política de duplicados y auditoría de fechas).
- [ ] Crear una clave de partido normalizada y una tabla de alias de equipos revisada.
- [ ] Regenerar los 5.235 registros fuente, conteos válidos y exclusiones desde archivos guardados.
- [ ] Comparar los partidos evaluables uno a uno para explicar la diferencia de 113.
- [ ] Reproducir métricas por partido, liga, temporada y modelo.
- [ ] Versionar código, manifiesto, configuración y reportes en GitHub.
- [ ] Mantener explícito que EV/ROI requiere cuotas históricas documentadas; no sustituirlas por cuotas actuales.

Hasta terminar estos pasos, los conteos y métricas históricos deben etiquetarse como **reportados previamente, pendientes de reproducción independiente**.
