# Resultado de reproducción independiente del backtest

**Fecha de ejecución:** 2026-10-14  
**Fuente efectivamente consultada:** `openfootball/football.json` en GitHub  
**Ventana:** temporadas 2023-24, 2024-25 y 2025-26; cinco ligas europeas  
**Estado:** reproducción computacional ejecutada sobre los JSON públicos consultados en esta fecha. Las métricas son exploratorias, no una validación de rentabilidad.

## 1. Fuente efectiva y discrepancia de procedencia

La versión anterior del script intentaba descargar CSV de DataHub, pero la conexión no funcionó. Para no dejar la auditoría bloqueada, se consultaron directamente los 15 JSON públicos de OpenFootball. La fuente debe citarse como OpenFootball, no como DataHub.

Rutas utilizadas:
- Premier League: `en.1.json`
- LaLiga: `es.1.json`
- Serie A: `it.1.json`
- Bundesliga: `de.1.json`
- Ligue 1: `fr.1.json`

Para cada liga se consultaron las carpetas `2023-24`, `2024-25` y `2025-26` del repositorio público `openfootball/football.json`.

## 2. Conteo de registros

| Control | Resultado |
|---|---:|
| Filas listadas en los 15 JSON | 5.256 |
| Filas con fecha, equipos y marcador final completo | 5.122 |
| Filas sin datos suficientes para el marcador final | 134 |
| Duplicados exactos detectados en la clave partido + marcador | 0 |
| Partidos con marcadores contradictorios para la misma clave | 0 |
| Partidos únicos limpios | 5.122 |
| Partidos evaluables con al menos 5 partidos previos para ambos equipos | 4.770 |
| Partidos omitidos por historial previo insuficiente | 352 |

El total de 5.122 con marcador completo no coincide con el total de 5.235 que aparecía en la auditoría anterior. Esto confirma que los conteos dependen de la versión de los archivos y del criterio de inclusión. No debe afirmarse que el universo histórico de 5.235 quedó reconciliado; para eso hacen falta los 15 archivos exactos que originaron ese reporte.

## 3. Métricas regeneradas

Se calculó un backtest cronológico que solo usa resultados de fechas anteriores a cada partido objetivo. Se compararon tres fórmulas 1X2 basadas en medias de goles recientes y una distribución Poisson. Los parámetros son fijos; no hubo optimización sobre el conjunto de prueba.

| Modelo | N | Exactitud 1X2 | Brier multiclase | Log loss |
|---|---:|---:|---:|---:|
| Multiplicadores 1,10 / 0,90 | 4.770 | 49,96 % | 0,6124 | 1,0213 |
| Neutral 1,00 / 1,00 | 4.770 | 48,97 % | 0,6209 | 1,0332 |
| Ajuste por localía/visita | 4.770 | 49,33 % | 0,6142 | 1,0247 |

### Resultados por temporada

| Temporada | N | Multiplicadores: exactitud | Neutral: exactitud | Ajuste localía: exactitud |
|---|---:|---:|---:|---:|
| 2023-24 | 1.510 | 50,26 % | 48,87 % | 49,27 % |
| 2024-25 | 1.665 | 48,11 % | 48,11 % | 47,81 % |
| 2025-26 | 1.595 | 51,60 % | 49,97 % | 50,97 % |

El mejor modelo por Brier global es el de multiplicadores fijos; por exactitud también obtiene el valor más alto en el total. No se debe interpretar esto como prueba de que el modelo sea fiable para apostar: falta comparar contra una línea base adecuada, medir calibración y hacer una evaluación de selección de apuestas sin fuga de información.

## 4. Por qué estas métricas difieren de reportes previos

El reporte anterior de 4.770 partidos mostraba 52,94 % de exactitud para el modelo de multiplicadores, mientras que esta ejecución obtuvo 49,96 %. Aunque el número de partidos evaluados coincide, las métricas no. Por ello no es correcto atribuir la diferencia solo a los 113 partidos discrepantes: hay diferencias adicionales en los datos de entrada, normalización, nombres de equipos, versión de la lógica o resultados guardados.

Los reportes anteriores no incluyen aquí un detalle completo que permita hacer una comparación partido a partido con la misma clave. Se necesita recuperar los CSV originales o las predicciones por partido del backtest que produjo aquellas cifras.

## 5. Limitaciones importantes

- No se descargaron ni verificaron cuotas históricas prepartido de Betano Colombia; por tanto no se calcularon EV ni ROI.
- Los nombres de equipos se usan tal como aparecen en la fuente; no se aplicó una tabla manual de alias.
- Los partidos sin marcador final completo se excluyeron.
- Las estadísticas de forma son una regla sencilla con parámetros fijos, no un modelo avanzado ni calibrado.
- Las cifras se calcularon sobre los datos consultados el 14 de octubre de 2026; una revisión futura debe volver a guardar archivos y hashes para fijar exactamente la versión de los datos.
- Las probabilidades 1X2 y las métricas no equivalen a una recomendación de apuesta.

## 6. Próximos pasos técnicos

1. Guardar los 15 JSON consultados, con SHA-256, dentro de un directorio de datos versionado o en un artefacto reproducible.
2. Corregir el manifiesto para registrar OpenFootball como fuente efectiva y separar cualquier fuente alternativa no descargada.
3. Obtener los resultados por partido del reporte previo y comparar la clave `liga + fecha + local + visitante` para explicar el cambio de métricas.
4. Añadir una línea base simple (por ejemplo, frecuencias históricas por liga) y evaluar calibración en un periodo de prueba separado.
5. Mantener EV/ROI como no evaluados hasta disponer de cuotas históricas auténticas.

**Conclusión:** el backtest se pudo volver a ejecutar sobre una fuente pública alternativa y produjo 4.770 predicciones evaluables. Sin embargo, las métricas previas no han sido reproducidas; la discrepancia de resultados sigue abierta y no se puede afirmar rentabilidad.
