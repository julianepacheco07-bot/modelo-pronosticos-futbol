# Diccionario operativo de mercados — Betano Colombia

Actualizado: 2026-10-18

## Reglas operativas inferidas del nombre
- **Ganar el partido / victoria:** el equipo elegido debe ganar al final del tiempo reglamentario más descuento, salvo que el mercado indique otra cosa.
- **Doble oportunidad 1X:** local gana o empata.
- **Doble oportunidad X2:** visitante gana o empata.
- **Doble oportunidad 12:** gana cualquiera de los equipos; el empate pierde.
- **Más de 1.5 goles:** deben anotarse al menos 2 goles en total.
- **Menos de 3.5 goles:** deben anotarse como máximo 3 goles en total.
- **Ambos equipos marcan — sí:** ambos anotan al menos un gol.
- **Ganar el partido o liderar por 2 goles:** regla reportada por el usuario: la apuesta se marca ganada en el momento en que el equipo elegido alcanza una ventaja de al menos dos goles; si no llega a esa ventaja, todavía puede ganar por victoria final. Un marcador posterior no revierte la liquidación anticipada reportada.

## Mercado “Ganar o liderar por 2 goles”
El evento a estimar es **victoria final O haber alcanzado una ventaja de dos o más goles en cualquier momento**. No debe confundirse con victoria simple ni doble oportunidad. Los dos sucesos se solapan y no deben sumarse sin corregir esa intersección.

La función `win_or_two_goal_lead` de `src/mercados_betano.py` estima este evento mediante una aproximación de llegadas de gol por minuto. Es exploratoria y no calibrada; no debe presentarse como probabilidad validada. Se necesita comparar con datos históricos de trayectorias de marcadores y calibrar fuera de muestra antes de usarla para decisiones reales.

## Evaluación y registro
- Probabilidad de equilibrio de cuota decimal: `1 / cuota`; no elimina el margen del operador.
- EV binario por unidad: `probabilidad × cuota - 1`, aplicable solo a liquidaciones de ganar/perder sin reembolso, pago parcial ni condiciones especiales.
- Cuota faltante: `CUOTA_PENDIENTE`; no equivale a NO BET.
- Probabilidad faltante: `ANALISIS_INSUFICIENTE`.
- Candidata: probabilidad estimada >=75%, cuota observada y EV positivo. El 75% es filtro de prioridad, no garantía.
- Combinadas: registrar cuota real observada y estimar probabilidad conjunta; no asumir independencia automáticamente.
- Si el texto de mercado no permite deducir inequívocamente la liquidación, registrar `PENDIENTE_DE_VERIFICACION` en vez de adivinar.

## Alcance de la regla
La regla de dos goles se documenta como aportada por el usuario para Betano Colombia. No se afirma que los términos oficiales de Colombia se hayan verificado independientemente, ni que las condiciones sean idénticas en otras jurisdicciones.

## Referencias
- Ayuda pública de Betano Ecuador sobre reglas de apuestas: https://support-ec.betano.com/hc/es-ec/articles/7874613484701--D%C3%B3nde-puedo-encontrar-la-secci%C3%B3n-de-Reglas-de-Apuestas
- Ayuda pública de Betano Brasil sobre “2 Gols de Vantagem” (referencia de otra jurisdicción, no prueba de las condiciones colombianas): https://support.betano.bet.br/hc/pt-br/articles/6414151241629-Como-funciona-a-oferta-2-Gols-de-Vantagem
