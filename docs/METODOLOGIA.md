# Metodología del Modelo de Pronósticos de Fútbol

**Estado:** protocolo propuesto; no equivale a resultados validados.  
**Repositorio:** `julianepacheco07-bot/modelo-pronosticos-futbol`

## 1. Propósito y principios

Construir un proceso reproducible para estimar probabilidades de mercados de fútbol antes del inicio del partido y validar su capacidad predictiva con resultados históricos. La evaluación económica de apuestas es una línea separada y prospectiva, basada en cuotas reales registradas desde el inicio de la simulación.

Principios obligatorios:
- No utilizar estadísticas en vivo del partido analizado para generar un pronóstico prepartido.
- No inventar datos, lesiones, alineaciones, cuotas, métricas ni resultados.
- Distinguir hechos confirmados, reportes periodísticos y rumores.
- No recomendar una apuesta solo porque la probabilidad estimada sea alta.
- No clasificar automáticamente todos los partidos como **NO BET**: evaluar cada caso y explicar qué evidencia falta o qué ventaja se estima.
- Las conclusiones históricas no garantizan resultados futuros.

## 2. Alcance de datos

El alcance de la línea base OpenFootball implementada cubre temporadas 2023-24, 2024-25 y 2025-26 de Premier League, LaLiga, Serie A, Bundesliga y Ligue 1. Los resultados de cada ejecución deben indicar las fuentes efectivamente recuperadas y su cobertura; una corrida incompleta no se acepta como backtest completo.

Antes del modelado se debe crear un inventario con:
- Competición, temporada y número de partidos.
- Identificador único del partido, fecha, local, visitante y marcador final.
- Fuente, URL o identificador de origen, fecha de descarga y licencia/condiciones de uso.
- Variables disponibles y porcentaje de valores ausentes.
- Duplicados, inconsistencias y partidos aplazados o incompletos.

No se publicará una cifra definitiva de partidos analizados hasta regenerar el conteo desde los archivos de origen. Los conteos comunicados en análisis previos fueron discrepantes y deben conciliarse.

## 3. Corte temporal y prevención de fuga de información

Cada pronóstico debe tener una hora de corte explícita anterior al inicio del partido. Solo se permiten datos que razonablemente estuvieran disponibles antes de ese corte.

- Ordenar los datos cronológicamente.
- No mezclar aleatoriamente partidos futuros en entrenamiento cuando se evalúa el desempeño temporal.
- Ajustar imputación, selección de variables, escalamiento y calibración únicamente con datos del conjunto de entrenamiento/validación correspondiente.
- Mantener fuera de entrenamiento el periodo final de prueba.
- Evitar variables que incorporen el resultado del partido, estadísticas posteriores al inicio o información publicada después del corte.
- Si se incorporan noticias del día, guardar fuente, hora y categoría: confirmado, reportado o rumor. Los rumores no deben tratarse como hechos.

## 4. Diseño de validación

Usar una evaluación temporal por etapas:
1. **Entrenamiento:** estimar parámetros con partidos anteriores.
2. **Validación:** elegir variables, modelos e hiperparámetros sin consultar el periodo final de prueba.
3. **Prueba fuera de muestra:** evaluar una sola vez el modelo seleccionado en un periodo posterior.
4. **Backtesting progresivo:** cuando sea viable, repetir el proceso con ventanas temporales sucesivas que simulen el uso real.

Las transformaciones y decisiones deben ajustarse dentro de cada ventana para evitar fuga de información. Documentar periodos, tamaño de cada conjunto, semilla cuando aplique y versiones de bibliotecas.

## 5. Modelos y comparaciones

Comenzar con líneas base transparentes antes de complejizar el modelo. Las alternativas pueden incluir probabilidades históricas por liga y temporada, modelos de goles como Poisson y modelos tabulares supervisados. La elección final depende de la cobertura, calidad de datos y validación; no se presupone que un modelo sea superior antes de probarlo.

Comparar todos los modelos en el mismo conjunto temporal y contra las mismas líneas base. Mantener un registro de variables, hiperparámetros, versión del código y fecha de ejecución.

## 6. Calidad de las probabilidades

Medir, cuando los datos lo permitan:
- **Log loss:** penaliza probabilidades muy seguras que resultan equivocadas.
- **Brier score:** mide el error cuadrático de las probabilidades.
- **Calibración:** comparar probabilidades previstas con frecuencias observadas en grupos de probabilidad.
- Métricas por liga, temporada y mercado, con tamaños de muestra visibles.

Para mercados mutuamente excluyentes, verificar que las probabilidades sumen aproximadamente 1. La calibración debe entrenarse con datos separados de la prueba. No publicar métricas sin especificar muestra, periodo, mercado y método.

## 7. Evaluación de apuestas

La decisión económica requiere una cuota real, específica para el mercado y obtenida antes del inicio. Para una selección de cuota decimal (o), probabilidad estimada (p) y retorno neto unitario en caso de acierto (o-1), el valor esperado neto por unidad apostada es:

`EV = p × (o - 1) - (1 - p)`

La cuota de equilibrio es `1 / o`. Cuando existan cuotas de todos los resultados del mercado, evaluar el margen de la casa y considerar su eliminación antes de comparar probabilidades. Registrar casa, cuota, hora de consulta y condiciones del mercado.

Las cuotas históricas no son requisito para entrenar, comparar ni validar la capacidad predictiva del modelo con resultados históricos. No deben buscarse ni reconstruirse cuotas pasadas. Desde el inicio de la simulación se registran cuotas realmente observadas; solo con esas cuotas prospectivas liquidadas se calcularán EV y ROI observados. Si no se verifica una cuota actual de Betano Colombia, se puede completar y reportar la evaluación probabilística, pero no afirmar valor esperado positivo ni inventar una cotización. El EV estimado con cuota actual es incierto y no constituye garantía.

Una probabilidad del 75% sirve como umbral de prioridad para revisar una selección; no es un mandato de apuesta ni sustituye el análisis de cuota, calibración, incertidumbre y riesgo.

## 8. Clasificación de cada análisis

- **APUESTA CANDIDATA:** datos suficientes, probabilidad evaluada, cuota verificada, ventaja estimada positiva y riesgos comunicados.
- **NO BET:** análisis suficientemente completo, pero no se observa ventaja convincente, la cuota no compensa el riesgo o la incertidumbre hace que la apuesta no sea atractiva.
- **ANÁLISIS INSUFICIENTE:** faltan datos deportivos esenciales o existe una limitación que impide sostener una conclusión probabilística. La ausencia de cuotas históricas nunca es motivo para bloquear el backtest predictivo. La ausencia de una cuota actual solo impide declarar EV/ROI para esa selección.

No usar **NO BET** como respuesta automática. Si faltan datos, usar **ANÁLISIS INSUFICIENTE** y especificar qué se necesita para resolverlo. Si hay una oportunidad respaldada, debe poder presentarse como **APUESTA CANDIDATA**, aunque nunca como certeza.

## 9. Mercados y presentación

Evaluar los mercados relevantes que cuenten con datos comparables y cuotas verificables; no limitarse por defecto al 1X2. No ampliar el número de selecciones solo para ofrecer una apuesta. Preferir una selección individual clara. Las combinadas requieren justificación cuantitativa y consideración de la dependencia entre eventos.

Para cada pronóstico registrar:
- Partido, competición, fecha y hora local.
- Mercado y selección.
- Probabilidad estimada y método/modelo.
- Cuota, casa y hora de consulta, o indicación explícita de que no se verificó.
- Probabilidad de equilibrio y EV solo cuando proceda.
- Clasificación final, principales argumentos, riesgos e incertidumbre.
- Fuentes de datos/noticias y hora de corte.
- Versión del modelo y referencia de la ejecución.

## 10. Auditoría, reproducibilidad y control de cambios

Cada ejecución debe guardar la configuración, periodos evaluados, conteos, fuentes, métricas y resultados. Los reportes deben poder regenerarse desde los archivos originales y el código versionado.

Antes de declarar el modelo validado:
- Conciliar los conteos de partidos y explicar exclusiones.
- Reproducir los resultados de backtesting desde una ejecución documentada.
- Comparar con líneas base.
- Verificar que no exista fuga de información.
- Reportar limitaciones, muestras pequeñas y resultados desfavorables.
- Mantener una separación clara entre métricas de predicción y rentabilidad de apuestas.

## 11. Estado actual y siguientes tareas

- [ ] Confirmar las cinco ligas incluidas en el alcance.
- [ ] Localizar y versionar los datos históricos con su procedencia.
- [ ] Auditar cobertura, duplicados, fechas y resultados.
- [ ] Conciliar los conteos históricos discrepantes.
- [ ] Implementar una línea base reproducible.
- [ ] Implementar partición temporal y métricas probabilísticas.
- [ ] Ejecutar backtesting fuera de muestra y publicar resultados verificables.
- [ ] Añadir pruebas automáticas y documentar cómo repetir la ejecución.

Hasta completar estas tareas, el protocolo y el repositorio son una base de trabajo, no una demostración de precisión ni rentabilidad.
