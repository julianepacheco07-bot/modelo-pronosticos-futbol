# Revisión postpartido — 18 de octubre de 2026
Zona horaria de referencia: America/Bogota
Fuente de resultados: resultados comunicados por el usuario; no verificados independientemente en esta entrada.

## Resultados comunicados
- Västerås SK 1-0 Mjällby AIF.
- PEC Zwolle 4-0 Go Ahead Eagles.

## Revisión de selecciones del cupón
- Västerås–Mjällby: se había considerado Mjällby o empate @1.62 y se descartó provisionalmente. Resultado 1-0 según usuario; la selección X2 habría perdido.
- Västerås–Mjällby: Más de 1.5 goles @1.25 fue la cuota informada después. Resultado 1-0; esta selección habría perdido. La cuota se registró como aportada por el usuario, sin confirmar hora de captura prepartido.
- PEC Zwolle–Go Ahead Eagles: se había considerado Go Ahead o empate @1.34. Con resultado 4-0 para Zwolle, la selección X2 habría perdido.

## Aprendizajes para el modelo
1. Registrar resultados reales y contrastarlos con cada mercado, no solo con el pronóstico principal.
2. No interpretar una cuota baja como garantía: Más de 1.5 @1.25 exige 80% de probabilidad para equilibrio y aun así puede fallar.
3. No concluir que una estimación está mal calibrada a partir de uno o dos partidos; acumular observaciones y medir Brier score, log loss y rentabilidad únicamente cuando haya probabilidades previas, cuotas y reglas de liquidación guardadas.
4. Separar dato aportado por usuario de dato verificado por fuente independiente.
5. Mantener la marca temporal de captura de cuota; si no se sabe si fue previa al inicio, no usarla como cuota histórica prepartido validada.
6. Para mercados de doble oportunidad, revisar la fortaleza del rival y la probabilidad de victoria del favorito contrario; no tratar X2 como apuesta segura por el nombre del equipo.

## Limitaciones
- Esta nota no demuestra causalidad ni justifica cambiar parámetros del modelo por sí sola.
- No se calculan métricas agregadas de rendimiento porque esta entrada no contiene el conjunto completo de probabilidades prepartido, cuotas verificadas, stake y liquidación de todas las selecciones.
