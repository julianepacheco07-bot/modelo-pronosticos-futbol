# Especificación de línea base canónica del backtest 1X2

Estado: propuesta de protocolo; no equivale a validación predictiva ni de rentabilidad.  
Fecha: 2026-10-14.

## 1. Objetivo

Establecer un protocolo único y versionado para que las futuras comparaciones sean repetibles, sin afirmar equivalencia con informes históricos cuando no hay predicciones originales por partido.

## 2. Ámbito

- Competiciones: Premier League, LaLiga, Serie A, Bundesliga y Ligue 1.
- Temporadas: 2023-24, 2024-25 y 2025-26.
- Mercado: resultado 1X2 a tiempo reglamentario.
- Fuente de datos inicial: OpenFootball football.json. Cada fichero se identifica mediante URL y SHA-256.
- No calcular EV ni ROI sin cuotas históricas verificadas y fechadas antes del inicio de cada partido.

## 3. Congelación de datos

Para cada ejecución conservar:
1. Los 15 JSON originales descargados, sin modificar.
2. SHA-256 de cada JSON, bytes, URL y hora de descarga UTC.
3. Versión/commit del código, versión de Python y dependencias.
4. XLSX de salida y manifiesto.
5. Número de filas leídas, inválidas, duplicadas, en conflicto, limpias, evaluables y omitidas.

Los hashes identifican archivos, pero no sustituyen una copia archivada. El artefacto de Actions tiene retención limitada; copiar los ficheros a almacenamiento permanente antes de que expire.

## 4. Limpieza y fixture key

- Validar fecha, equipos y goles enteros no negativos.
- No imputar resultados faltantes.
- Eliminar duplicados exactos conservando registro de auditoría.
- Excluir y reportar todos los registros de un fixture cuya misma liga, fecha, local y visitante tenga marcadores contradictorios.
- Fixture key canónica: competición + fecha local del partido + nombre normalizado local + nombre normalizado visitante. Guardar también los nombres originales.
- No fusionar partidos por coincidencia aproximada de nombres sin una tabla de alias revisada y versionada.

## 5. Corte temporal anti-fuga

Para predecir un partido en fecha D, usar únicamente partidos de la misma competición cuya fecha sea estrictamente anterior a D. Ningún partido de la misma fecha puede incorporarse al historial, aunque se conozca su resultado o la hora de inicio. Las transformaciones y cualquier calibración se ajustan exclusivamente en datos anteriores al período evaluado.

## 6. Modelo de referencia (baseline)

- Para cada equipo, calcular GF y GA medios de sus últimos cinco partidos previos, sin filtrar por localía para la referencia general.
- Exigir al menos cinco partidos previos por cada equipo; si falta historial, marcar como omitido con motivo.
- Intensidades neutrales: lambda_local = (GF_local + GA_visitante)/2; lambda_visitante = (GF_visitante + GA_local)/2.
- Variante multiplicadores: lambda_local × 1,10 y lambda_visitante × 0,90. Esta variante es una hipótesis experimental, no una ventaja demostrada.
- Variante localía: usar últimos cinco partidos generales por equipo; sustituir el promedio por localía específica solo si existen al menos tres partidos previos del equipo en ese rol. Documentar esta regla.
- Probabilidades de goles: Poisson para 0..12 goles, normalizando explícitamente la masa truncada. Sumar probabilidades para obtener 1/X/2 y normalizar la terna por errores numéricos.
- Desempate de la clase predicha: orden fijo 1, X, 2.
- No aplicar calibración de temperatura a la línea base. Cualquier calibrador debe ajustarse en una ventana anterior independiente y compararse con el baseline sin calibrar.

## 7. Evaluación

Reportar por modelo y por liga-temporada:
- N de partidos evaluados y proporción omitida.
- Exactitud 1X2.
- Brier multiclase: suma de errores cuadrados de las tres probabilidades por partido, promediada.
- LogLoss: negativo del logaritmo de la probabilidad asignada al resultado real, con piso numérico documentado.
- Matriz de confusión y calibración por bandas, con cantidad de casos en cada banda.
- Incertidumbre de las métricas mediante intervalos de confianza; comparar modelos sobre el mismo conjunto de fixtures.
- Baseline adicional: frecuencia histórica de clases estimada solo con entrenamiento pasado. No seleccionar modelos solo por exactitud.

## 8. Pruebas obligatorias

1. No hay datos de historial con fecha >= fecha del partido evaluado.
2. Las probabilidades 1X2 son finitas, están en [0,1] y suman 1.
3. Poisson 0..12 es finita y suma 1 después de renormalizar.
4. Duplicados exactos retirados y conflictos excluidos.
5. El fixture key no fusiona local/visitante invertidos.
6. La evaluación es determinista para los mismos datos y commit.
7. Todas las comparaciones entre modelos utilizan exactamente los mismos fixtures.
8. Cambiar el resultado de un partido futuro no altera predicciones de partidos anteriores.
9. Fuentes incompletas o errores de descarga provocan estado fallido o explícitamente parcial, nunca un éxito silencioso.

## 9. Reconciliación histórica

Los agregados anteriores no son suficientes para una comparación fixture-a-fixture. Para reproducir una versión antigua se requiere al menos la predicción por partido, fecha de corte, probabilidades, resultado real, fuente de datos y parámetros. Si esos artefactos no existen, la comparación histórica exacta es imposible; registrar una nueva línea base y no inferir causas no verificadas.

## 10. Criterios de aceptación

- Todas las fuentes previstas están archivadas y sus hashes coinciden.
- Pruebas automáticas pasan.
- Ninguna fuga temporal.
- Todas las métricas se generan desde el mismo detalle por partido y pueden recalcularse.
- Cualquier omisión está listada y explicada.
- La comparación de modelos se realiza sobre los mismos fixtures.
- No se afirma rentabilidad sin cuotas históricas verificadas y evaluación fuera de muestra.

## 11. Limitaciones actuales

Este protocolo es una especificación de trabajo. Su publicación no implica que cada prueba esté implementada ni que el backtest actual ya cumpla todos los criterios. El estado de cada criterio debe registrarse por separado en cada ejecución.
