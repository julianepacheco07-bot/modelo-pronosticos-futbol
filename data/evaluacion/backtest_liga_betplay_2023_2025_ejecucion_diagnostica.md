# Ejecución diagnóstica del backtest — Liga BetPlay 2023–2025

**Estado: ejecución exploratoria completada sobre datos descargados desde OpenFootball; recalibración NO aprobada.**  
**Fecha de ejecución:** 19 de octubre de 2026.

## Fuente y cobertura parseada

Se recuperaron los archivos de texto públicos de OpenFootball desde sus URLs raw. El parser actual encontró:

| Archivo fuente | Partidos con marcador parseados |
|---|---:|
| 2023 | 433 |
| 2024 | 409 |
| 2025 (parcial) | 167 |
| **Total** | **1.009** |

El procedimiento generó predicciones para **949 partidos** después de exigir al menos cuatro partidos previos por equipo. El rango de predicciones va del 18 de febrero de 2023 al 4 de mayo de 2025.

Fuentes:
- https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2023_co1.txt
- https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2024_co1.txt
- https://raw.githubusercontent.com/openfootball/south-america/master/colombia/2025_co1.txt

## Método ejecutado

- Orden cronológico por fecha.
- Para cada equipo, últimos 10 resultados previos, con un mínimo de 4 partidos.
- Tasas de goles a favor y en contra por equipo, suavizadas hacia promedios generales de goles en partidos previos (fuerza de suavizado 4).
- Distribución de marcadores por Poisson independiente, truncada a 12 goles y renormalizada.
- Mercados calculados desde la matriz de marcadores: 1X2, Over 1.5, Under 3.5 y ambos equipos marcan.

Este es un **modelo diagnóstico simple**: no incluye ajuste explícito de localía dentro de la forma de cada equipo, alias de clubes verificados, intervalos de confianza ni comparación contra una línea base rolling ya auditada.

## Métricas observadas

| Mercado | N | Brier | Log loss | Probabilidad media | Frecuencia observada |
|---|---:|---:|---:|---:|---:|
| 1X2 (multiclase) | 949 | 0,6271 | 1,0419 | — | Acierto del signo: 47,10 % |
| Over 1.5 | 949 | 0,2353 | 0,6644 | 65,63 % | 63,54 % |
| Under 3.5 | 949 | 0,1447 | 0,4659 | 80,77 % | 82,82 % |
| Ambos marcan | 949 | 0,2505 | 0,6941 | 44,11 % | 44,47 % |

## Interpretación prudente

- El modelo sobreestima la frecuencia de Over 1.5 en aproximadamente 2,09 puntos porcentuales en esta muestra.
- Sobreestima la probabilidad de Under 3.5 en promedio en aproximadamente 2,05 puntos porcentuales (frecuencia observada mayor que probabilidad media, por lo que en realidad **subestima** el Under 3.5 en ~2,05 puntos).
- Ambos marcan queda muy cerca en promedio, con diferencia de ~0,04 puntos porcentuales.
- La exactitud 1X2 de 47,10% por sí sola no demuestra calidad: debe compararse con una línea base y acompañarse de Brier/Log Loss y calibración por bandas.

## Advertencias de calidad

1. Los 433 y 409 partidos parseados en 2023 y 2024 pueden incluir cuadrangulares/playoffs además de fases regulares; confirmar cobertura y duplicados antes de aprobar resultados.
2. El archivo 2025 disponible en esta ruta solo llega a mayo en la versión consultada. No representa la temporada completa.
3. Nombres de equipos pueden cambiar entre temporadas; falta normalización de alias.
4. El parser identifica fechas y resultados por patrones de texto. Hay que auditar partidos muestreados contra la fuente y detectar fechas omitidas.
5. No se calcularon intervalos de confianza ni se comparó contra una línea base de frecuencias rolling en esta ejecución.
6. No se incorporaron cuotas prepartido; no hay evaluación de valor esperado ni ROI.
7. Estas métricas no justifican cambiar parámetros ni trasladar automáticamente el modelo a decisiones de apuesta.

## Decisión

**No aplicar recalibración automática aún.** Esta ejecución permite detectar una discrepancia agregada para Over 1.5, pero antes de corregirla se debe:
- validar cobertura y parseo;
- normalizar equipos;
- implementar una línea base rolling usando solo resultados previos;
- reportar diagramas/tablas de calibración y bootstrap temporal;
- comparar candidatos con validación rolling-origin y test final reservado.

Hasta completar estos controles, el modelo para Liga BetPlay permanece experimental.
