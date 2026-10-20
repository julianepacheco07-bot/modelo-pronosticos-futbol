# Backtest diagnóstico — Liga BetPlay 2023–2025

**Estado: BLOQUEADO PARA CONCLUSIONES. No aprobar recalibración ni usar estos resultados para recomendar apuestas.**

## Hallazgo de auditoría

La fuente OpenFootball de 2025 declara **200 partidos**, pero el informe previo contabilizó solo **167**. Esto revela una discrepancia de cobertura que debe resolverse antes de considerar fiables las métricas agregadas. Los datos de 2023 y 2024 también deben contrastarse automáticamente con el encabezado de cada archivo.

- Fuente 2023: https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2023_co1.txt
- Fuente 2024: https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2024_co1.txt
- Fuente 2025: https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2025_co1.txt

## Métricas previas: solo referencia no validada

El informe anterior reportó 995 predicciones evaluadas y estos resultados:

| Mercado | Brier modelo | Brier línea base | Log loss modelo | Log loss línea base |
|---|---:|---:|---:|---:|
| 1X2 multiclase | 0,6256 | 0,6379 | 1,0399 | 1,0569 |
| Over 1.5 | 0,2343 | 0,2321 | 0,6623 | 0,6571 |
| Under 3.5 | 0,1474 | 0,1454 | 0,4723 | 0,4667 |
| Ambos marcan | 0,2506 | 0,2488 | 0,6943 | 0,6907 |

**No deben interpretarse como resultados confirmados** hasta volver a ejecutar el backtest después de corregir la cobertura y reconciliar los marcadores parseados con los conteos declarados por la fuente. En particular, no calculo intervalos de confianza ni calibración por bandas sobre una muestra cuya integridad todavía está en duda.

## Corrección aplicada al script

El script se actualizó para:
1. Escribir los artefactos en las rutas diagnósticas ya publicadas, evitando que una ejecución genere archivos con nombres distintos.
2. Leer el número de partidos declarado en el encabezado de cada fuente.
3. Registrar el conteo declarado y el parseado, marcar si coinciden y emitir una advertencia si hay discrepancias.

Código actualizado: https://github.com/julianepacheco07-bot/modelo-pronosticos-futbol/blob/main/src/backtest_liga_betplay.py

## Siguiente criterio de aceptación

No cerrar esta auditoría hasta que:
- los conteos parseados coincidan con los encabezados de la fuente o cada diferencia esté explicada;
- se inspeccionen nombres de equipos, fechas y partidos duplicados;
- se vuelva a calcular el backtest con un solo procedimiento reproducible;
- se publiquen calibración por bandas e intervalos de confianza temporales;
- se mantenga separado el análisis de probabilidades del ROI, que requiere cuotas prepartido archivadas.

**Limitación operativa:** pude modificar el archivo en GitHub, pero no ejecutar aquí el script Python del repositorio. Por tanto, no afirmo que la corrección ya haya sido ejecutada ni que las métricas estén recalculadas.
