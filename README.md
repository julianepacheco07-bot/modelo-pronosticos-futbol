# Modelo de Pronósticos de Fútbol

**Repositorio:** `julianepacheco07-bot/modelo-pronosticos-futbol`

## Objetivo
Construir y evaluar un modelo de pronósticos de fútbol prepartido, con validación temporal y decisiones de simulación basadas en probabilidades y cuotas realmente observadas.

## Regla definitiva para las cuotas
- **El histórico de cuotas empieza ahora, desde el inicio de nuestra simulación.**
- No buscar, comprar, importar ni reconstruir cuotas históricas anteriores al inicio de este registro.
- En cada jornada, guardar las cuotas actuales realmente observadas, casa de apuestas, mercado, selección, fecha/hora de captura, hora del partido, probabilidad del modelo, cuota justa y EV estimado.
- No atribuir a Betano cuotas de otras casas. Si no se puede verificar una cuota, registrar que no está disponible y continuar con el resto del análisis.
- Tras cada partido, registrar resultado y liquidar unidades virtuales. Calcular ROI acumulado únicamente con selecciones registradas y liquidadas.
- El backtest de resultados deportivos históricos puede seguir utilizando marcadores anteriores para evaluar predicción; eso **no** autoriza a reconstruir cuotas pasadas.
- El registro prospectivo se guarda en `data/simulacion/registro_cuotas.csv`, mediante `src/registrar_cuota_simulacion.py`.

## Alcance y reglas
- Analizar partidos antes del inicio; no usar estadísticas en vivo del partido que se pronostica.
- Las noticias del día pueden aportar contexto prepartido, distinguiendo hechos confirmados, reportes y rumores.
- Evaluar mercados pertinentes; no limitar automáticamente el análisis al 1X2.
- Separar entrenamiento, validación y prueba por tiempo para evitar fuga de información.
- Registrar fuentes, fecha/hora de consulta, hora de corte, versión del modelo y configuración.
- Comparar con líneas base y medir Brier score, log loss, calibración y, cuando existan cuotas capturadas, EV y ROI.
- No presentar resultados históricos como garantía de rentabilidad futura.
- Clasificar cada evaluación como **APUESTA CANDIDATA**, **NO BET** o **ANÁLISIS INSUFICIENTE** según evidencia; no forzar NO BET por defecto.
- Una probabilidad estimada del 75% es una señal de prioridad, no razón suficiente para apostar: también se requiere precio observado, EV positivo y evaluación de riesgo.
- Las combinadas requieren probabilidad conjunta estimada y cuota combinada observada; nunca inventar precios.
- Mantener separados datos prepartido y en vivo.

## Estructura
- `docs/METODOLOGIA.md`: protocolo de análisis y evaluación.
- `data/`: datos y procedencia; no subir secretos ni datos con restricciones de licencia.
- `src/`: modelo y utilidades, incluidas funciones de mercados en `mercados_betano.py`.
- `tests/`: pruebas unitarias; ejecutar con `python -m unittest discover -s tests`.
- `tests/`: pruebas reproducibles.
- `reports/`: resultados con parámetros y fecha.

## Estado
- [x] Repositorio público creado.
- [x] Backtest exploratorio de mercados de goles en Colombia, Brasil y Argentina (temporadas 2023–2025).
- [x] Registro prospectivo de cuotas desde el inicio de la simulación.
- [x] Añadidas funciones exploratorias para interpretar mercados comunes y modelar “ganar o liderar por 2 goles” (`src/mercados_betano.py`).
- [x] Añadidas pruebas unitarias para interpretación de mercados, probabilidades, EV y tratamiento de cuotas faltantes (`tests/test_mercados_betano.py`).
- [ ] Validar calibración del modelo fuera de muestra.
- [ ] Registrar y liquidar las primeras selecciones simuladas para iniciar las métricas de EV/ROI observados.

## Reproducibilidad
Todo resultado debe poder regenerarse a partir de datos, código y configuración registrados. Si falta una cuota actual o una fuente, declararlo como no disponible sin bloquear el resto del flujo y sin inventar datos.
