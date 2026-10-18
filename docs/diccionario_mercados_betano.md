# Diccionario técnico de mercados — Betano Colombia
## Entrada: “Ganar el partido o liderar por 2 goles”
Fecha documentada: 2026-10-18
Fuente de la regla operativa: explicación del usuario a partir de su interfaz de Betano; pendiente de cotejo con las reglas oficiales de liquidación.

### Significado operativo informado
La selección gana si el equipo elegido gana el partido **o si llega a estar ganando por una diferencia de dos goles durante el encuentro**. En este segundo caso, Betano marca la apuesta como ganada anticipadamente, según la explicación del usuario. Si ya fue liquidada como ganadora al alcanzar esa ventaja, un resultado posterior que reduzca o elimine la ventaja no revierte esa liquidación, según lo informado.

### Consecuencias para el análisis
- No tratar este mercado como victoria simple ni como doble oportunidad.
- Modelar el evento como: equipo gana al final **O** equipo alcanza una ventaja de al menos dos goles en algún momento antes de terminar el partido.
- Estos sucesos se solapan; calcular la probabilidad del evento combinado contando una sola vez los partidos donde se cumplen ambas condiciones.
- No estimar la probabilidad de este mercado usando únicamente la probabilidad 1X2.
- Comparar la cuota con la probabilidad del evento completo; cuota justa = 1 / probabilidad estimada, y EV simple = p × cuota − 1 solo si la liquidación es binaria y sin condiciones adicionales.
- Registrar por separado cuota, hora de captura, reglas de liquidación y fuente. Si la regla solo fue descrita por el usuario, marcarla como “regla reportada por usuario; pendiente de verificación oficial”.
- No asumir que el mismo texto tiene idéntica liquidación en otros operadores o en otros mercados.

### Ejemplos del boleto del 18-10-2026
- Molde FK vs IK Start — Molde gana o lidera por 2 goles, cuota reportada 1.34.
- Nottingham Forest vs Arsenal — Arsenal gana o lidera por 2 goles, cuota reportada 1.62.

### Limitación
Esta entrada documenta la interpretación operativa aportada por el usuario. Antes de automatizar la liquidación del modelo, contrastar con los términos oficiales de Betano Colombia y conservar evidencia de la regla vigente.
