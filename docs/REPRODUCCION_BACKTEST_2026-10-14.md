# Reproducción independiente de datos y backtest (14 de octubre de 2026)

## Alcance y fuentes
Se consultaron directamente los 15 archivos JSON públicos de `openfootball/football.json`, para Premier League (`en.1`), LaLiga (`es.1`), Serie A (`it.1`), Bundesliga (`de.1`) y Ligue 1 (`fr.1`), temporadas 2023-24, 2024-25 y 2025-26. La documentación del proyecto OpenFootball identifica estos archivos como datos públicos de partidos y resultados y señala una dedicación de dominio público.

## Conteo reproducido desde las fuentes consultadas
- Fixtures en los 15 archivos: **5.256**.
- Filas con fecha, equipos y marcador final válido: **5.122**.
- Filas sin datos de marcador/fecha/equipo suficientes: **134**.
- Duplicados exactos encontrados: **0**.
- Conflictos de marcador para una misma clave liga-fecha-local-visitante: **0**.
- Partidos evaluables por el protocolo de forma reciente (mínimo cinco partidos previos por equipo y fecha estrictamente anterior): **4.770**.
- Partidos omitidos por historial previo insuficiente: **352**.

Los 134 registros incompletos se refieren a filas del fixture sin un marcador final usable; no se incorporan al backtest. El conteo se calculó en esta revisión leyendo los 15 JSON; el script versionado permite repetirlo desde los archivos guardados y genera SHA-256 por fuente.

## Métricas del backtest calculadas en esta revisión
Modelo de forma reciente, 1X2, distribución de Poisson con máximo de 10 goles por equipo, y probabilidades normalizadas. Métricas agregadas sobre los 4.770 partidos evaluables:

| Modelo | Exactitud 1X2 | Brier multiclase | Log loss |
|---|---:|---:|---:|
| Multiplicadores 1,10/0,90 | 49,96 % | 0,61241 | 1,02134 |
| Neutral 1,00/1,00 | 48,97 % | 0,62090 | 1,03324 |
| Ajuste local/visitante | 49,33 % | 0,61420 | 1,02466 |

Son métricas exploratorias del cálculo reproducido en esta revisión, no evidencia de rentabilidad. No se calcularon ROI, EV ni rendimiento de apuestas porque no se verificaron cuotas históricas prepartido.

## Discrepancia con los reportes previos
El conteo de 4.770 evaluables coincide con el reporte anterior que registraba 4.770, pero **las métricas no coinciden** con el resumen previo (que reportaba 52,94 % de exactitud, Brier 0,59368 y log loss 0,99594 para el modelo 1,10/0,90). Por tanto, no es correcto afirmar que se reprodujeron esos valores anteriores. Las posibles causas a investigar son versiones diferentes de los archivos fuente, diferencias en nombres/normalización de equipos, código ejecutado distinto al guardado o cambios de la fuente desde la ejecución original. El informe previo de 4.883 evaluables tampoco queda reproducido por este conjunto actual.

## Limitación importante del corte temporal
El cálculo aquí fue hecho con los archivos públicos consultados el 14-10-2026. El repositorio upstream puede cambiar. Para una reproducción histórica exacta se deben guardar las 15 respuestas JSON originales, sus SHA-256 y la versión del código usado en cada corrida. El script nuevo descarga y conserva los archivos y el manifiesto local para futuras ejecuciones.

## Estado
- [x] Consultar los 15 archivos de las cinco ligas y tres temporadas.
- [x] Recalcular el conteo de fixtures, resultados válidos, omitidos y evaluables.
- [x] Recalcular métricas agregadas del backtest.
- [x] Documentar que las métricas no coinciden con el reporte anterior.
- [ ] Ejecutar el script en un entorno de usuario con conexión y guardar las 15 fuentes con sus hashes.
- [ ] Comparar las claves partido a partido con el detalle original que generó el reporte anterior (no se localizó en el repositorio ni en los reportes resumidos).
- [ ] Determinar la causa exacta de la diferencia de métricas y corregirla antes de declarar el modelo validado.
- [ ] Incorporar cuotas históricas prepartido verificables si se quiere evaluar ROI/EV.

## Referencias
- Repositorio y documentación de OpenFootball: https://github.com/openfootball/football.json
- Ejemplo de fuente EPL 2023-24: https://raw.githubusercontent.com/openfootball/football.json/master/2023-24/en.1.json
- EPL 2024-25: https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json
- EPL 2025-26: https://raw.githubusercontent.com/openfootball/football.json/master/2025-26/en.1.json
