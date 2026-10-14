# Modelo de Pronósticos de Fútbol

**Repositorio:** `julianepacheco07-bot/modelo-pronosticos-futbol`

## Objetivo
Construir y evaluar un modelo de pronósticos de fútbol prepartido, con backtesting temporal, probabilidades calibradas y decisiones de apuesta condicionadas a cuotas verificadas y valor esperado positivo.

## Alcance inicial
- Temporadas objetivo: 2023-24, 2024-25 y 2025-26.
- Utilizar datos históricos para modelar y evaluar; no usar estadísticas en vivo del partido que se pronostica.
- Las noticias del día pueden aportar contexto prepartido, distinguiendo hechos confirmados, reportes y rumores.
- Evaluar mercados pertinentes; no limitar automáticamente el análisis al 1X2.
- Verificar las cuotas de Betano Colombia antes de calcular valor esperado. Nunca inventar cuotas.

## Reglas de análisis
1. Separar entrenamiento, validación y prueba por tiempo para evitar fuga de información.
2. Registrar fuentes, fecha de consulta, hora de corte prepartido, versión del modelo y configuración.
3. Comparar con líneas base y medir calidad probabilística (Brier score, log loss), calibración y rendimiento económico bajo supuestos realistas.
4. No presentar resultados históricos como garantía de rentabilidad futura.
5. Clasificar cada evaluación como **APUESTA CANDIDATA**, **NO BET** o **ANÁLISIS INSUFICIENTE**, según la evidencia. No forzar NO BET por defecto.
6. Una probabilidad estimada del 75% es una señal de prioridad, no una razón suficiente para apostar: también se requieren cuota verificada, valor esperado positivo y evaluación de riesgo.
7. Preferir una selección clara; recomendar combinadas solo con justificación cuantitativa.
8. Mantener separados los datos prepartido y en vivo.

## Estructura prevista
- `README.md`: objetivo, reglas y estado.
- `docs/METODOLOGIA.md`: protocolo de análisis y evaluación.
- `data/`: datos y documentación de procedencia; no subir secretos ni datos con restricciones de licencia.
- `src/`: código del modelo y utilidades.
- `tests/`: pruebas reproducibles.
- `reports/`: resultados de backtesting con parámetros y fecha.

## Estado del proyecto
- [x] Repositorio público creado.
- [ ] Incorporar los datos de origen y documentar su procedencia.
- [ ] Regenerar el backtest desde código con partición temporal y métricas verificables.
- [ ] Conciliar los conteos históricos discrepantes antes de publicar cifras definitivas.
- [ ] Añadir pruebas automáticas y un comando reproducible de ejecución.

## Reproducibilidad
Todo resultado debe poder regenerarse a partir de datos, código y configuración registrados. Si falta una fuente o un archivo, declararlo como pendiente en lugar de inferir o inventar resultados.
