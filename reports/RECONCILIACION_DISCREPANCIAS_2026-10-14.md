# Reconciliación de discrepancias del backtest — 2026-10-14

## Conclusión ejecutiva

La discrepancia aún no puede cerrarse como una reproducción exacta. Los reportes históricos disponibles y el nuevo cálculo no comparten toda la configuración ni se ha podido comparar una tabla de predicciones por partido de ambas ejecuciones.

## Diferencias confirmadas en los artefactos

1. **Datos de entrada:** un reporte anterior registra 5.235 partidos con marcador final utilizable; la consulta posterior de los 15 JSON registra 5.122. Los 113 registros adicionales no están identificados partido por partido en los artefactos consultados. Los datasets públicos pueden cambiar, por lo que se necesitan los archivos exactos o snapshots de la ejecución histórica.
2. **Partidos evaluables:** ambos cálculos registran 4.770 evaluables y 352 omitidos, pero el número de evaluables coincidente no demuestra que sean los mismos partidos.
3. **Parámetros de goles:** la auditoría histórica documenta una matriz Poisson hasta 12 goles; el script de la segunda ejecución utiliza un máximo de 10 goles.
4. **Calibración:** el reporte anterior documenta temperatura T=0,80, seleccionada solo en entrenamiento y aplicada a la prueba 2025-26. El script nuevo no aplica calibración.
5. **Exactitud no reconciliada:** el informe anterior registra 52,935% y el nuevo cálculo 49,96%. La temperatura de calibración no explica por sí sola esta diferencia porque el escalado de probabilidades no suele cambiar la clase argmax. Es probable que haya diferencias en datos de entrada, identidad de equipos, fórmulas o historial utilizado, pero no es posible asignar la causa exacta sin las predicciones por partido.
6. **Persistencia GitHub:** una consulta de metadatos del repositorio devolvió tamaño 0 aunque las acciones de archivo devolvieron contenido. Por tanto, no se debe asumir que el repositorio remoto contiene efectivamente los artefactos hasta confirmar su árbol y commits en GitHub.

## Qué queda demostrado y qué no

- El reporte previo contiene las cifras 5.235 / 4.883 y el reporte más reciente contiene 5.122 / 4.770.
- No se ha reconciliado la identidad de los 113 partidos.
- No se ha reproducido la exactitud histórica de 52,935% con la nueva ejecución.
- No hay cuotas históricas verificadas, así que EV/ROI siguen sin calcular.
- Las métricas actuales deben etiquetarse como exploratorias, no como resultado validado.

## Procedimiento correcto para cerrar la discrepancia

1. Congelar los 15 archivos exactos usados en la auditoría histórica y los 15 usados en la nueva ejecución.
2. Crear una clave normalizada por liga, fecha, local y visitante; auditar alias y cambios de nombre.
3. Comparar los conjuntos de claves y listar las 113 filas presentes solo en un conjunto, además de los marcadores faltantes.
4. Ejecutar una sola implementación con la misma regla de historial, corte por fecha, límite de goles, fórmulas y calibración documentadas.
5. Guardar predicciones por partido, probabilidades, métricas y SHA-256 de cada fuente.
6. Aceptar la reconciliación solo cuando los conteos y métricas puedan regenerarse desde esos artefactos.

No se deben declarar resueltas las discrepancias ni publicitar rentabilidad hasta terminar este procedimiento.
