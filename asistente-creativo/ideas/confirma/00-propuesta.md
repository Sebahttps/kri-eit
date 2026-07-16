# Confirma — Propuesta completa de Kri-ai

> Segunda propuesta desarrollada por Kri-ai (julio 2026), elegida por el usuario entre
> 3 opciones con tecnología como palanca. Contexto real: Santiago u otra ciudad grande
> de Chile; el dueño no programa pero domina herramientas digitales (no-code, IA,
> planillas, redes); presupuesto inicial $500.000–$2.000.000 CLP; dedicación tiempo
> completo. Supuesto adicional: tiene computador y smartphone propios. Todos los
> montos son estimaciones para Chile 2026 salvo que se indique lo contrario — validar
> antes de comprometer plata.

## 1. La idea

**Confirma — recuperamos las horas médicas que los centros de salud de barrio pierden
por inasistencia.**

Servicio administrado (no software que se instala, sino un servicio que tú operas con
herramientas no-code) que confirma citas, envía recordatorios, gestiona
reagendamientos y **rellena los cupos liberados con la lista de espera** de dentistas,
kinesiólogos, podólogos, fonoaudiólogos, nutricionistas y centros médicos chicos. El
cliente no compra tecnología: compra horas recuperadas, es decir, facturación que hoy
se le evapora.

- **Necesidad que resuelve:** salud, primera necesidad. La inasistencia a horas
  médicas ("no-show") se estima entre 15% y 25% de las citas agendadas en Chile
  (orden de magnitud citado públicamente en el sector; **estimación a validar por
  rubro y comuna en los pilotos**). Cada cupo perdido son dos daños: un paciente que
  no se atendió (y otro en lista de espera que sí quería esa hora) y plata que el
  centro no facturó. Es un problema común, viejo y mal resuelto: la secretaria no
  alcanza a llamar a todos, y si llama, lo hace una vez y sin rellenar el cupo.
- **Rol exacto de la tecnología:** WhatsApp Business API + automatizaciones no-code
  (Make) + planilla estructurada + IA para redactar y clasificar respuestas. La
  tecnología baja el costo de hacer 300 confirmaciones al mes a casi cero; el negocio
  es el servicio y el resultado medible, no la herramienta. Nada requiere programar.
- **Por qué prevalecerá:** la atención de salud presencial no desaparece en 10 ni en
  20 años; la demanda supera a la oferta y la inasistencia es un problema de
  comportamiento humano, no de tecnología. Cambiará el canal (hoy WhatsApp, mañana
  otro), pero la necesidad de llenar la agenda de un profesional de la salud es
  permanente.
- **Riesgo de moda tecnológica, declarado:** dependencia de WhatsApp como canal y de
  los precios de Meta para conversaciones API. Mitigación: el servicio es
  canal-agnóstico (funciona por SMS o llamada si hiciera falta) y el contrato con el
  cliente promete "horas recuperadas", no "mensajes de WhatsApp".
- **Veta:** problema común **mal resuelto**. Los software de agenda (AgendaPro,
  Dentalink y similares) mandan un recordatorio y ahí terminan: nadie gestiona las
  respuestas, nadie reagenda, y sobre todo **nadie rellena el cupo liberado**. Ese
  último tramo — el que genera la plata — es humano + automatización, y es tu nicho.

## 2. Cómo venderla (plan comercial)

### Cliente objetivo

- **Quién:** dueños de consultas y centros de salud chicos (1 a 5 profesionales):
  dentistas, kinesiólogos, podólogos clínicos, fonoaudiólogos, nutricionistas,
  psicólogos (con cuidado especial de datos), centros médicos de barrio. En Santiago
  hay miles; abundan en torno a metros, avenidas comerciales y barrios cívicos de
  cada comuna.
- **Dónde y cuándo compra:** en su propia consulta, entre pacientes o al final de la
  jornada. Decide el dueño (el profesional mismo o el administrador); ciclo de
  decisión corto si el piloto es gratis.
- **Qué le duele:** ve la agenda llena en la mañana y sillas vacías en la tarde. Sabe
  cuánto vale cada hora perdida ($25.000–$60.000 por atención según especialidad,
  estimación) pero no tiene a nadie que persiga confirmaciones ni lista de espera.
- **Cuánto gasta hoy:** el tiempo de la secretaria (si tiene) o nada — pierde en
  silencio. Algunos pagan software de agenda ($30.000–$70.000/mes estimado) que
  recuerda pero no recupera.

### Propuesta de valor

**"Le recupero las horas que hoy pierde por pacientes que no llegan; si no le
recupero al menos el doble de mi tarifa en atenciones, ese mes no me paga."**

Diferenciación frente a las alternativas actuales:

- Frente a la secretaria: ella confirma a algunos, una vez, y no rellena cupos.
  Confirma confirma a todos, dos veces, reagenda y rellena — y la secretaria queda
  libre para el mesón.
- Frente al software de agenda: el software manda un mensaje; nadie lee las
  respuestas ni gestiona el cupo liberado. Confirma es servicio administrado con un
  humano responsable y un reporte mensual de plata recuperada.
- Prueba: el piloto gratis de 2 semanas con medición antes/después. El dato vende solo.

### Estructura de precios (estimaciones; validar disposición a pagar en pilotos)

| Plan | Qué incluye | Precio mensual por centro (hasta ~250 citas/mes) |
|---|---|---|
| **Básico "Confirma"** | Confirmación al agendar + recordatorios 48 h y 3 h antes + gestión de respuestas y reagendamiento simple + reporte mensual | **$60.000 + IVA** |
| **Completo "Confirma + Relleno"** | Todo lo del Básico + lista de espera administrada + relleno automático de cupos liberados + reporte de facturación recuperada | **$110.000 + IVA** |

- **Lógica del precio:** valor percibido. Recuperar 3–4 atenciones al mes ya paga el
  plan Completo; la meta es recuperar 8–15. Está bajo el costo de media jornada de
  secretaria y en el rango de un software de agenda, entregando lo que el software no da.
- **Excedente de volumen:** sobre 250 citas/mes, +$20.000 por cada 100 citas
  adicionales (cubre el costo de conversaciones de la API).
- **Garantía comercial:** si el reporte mensual no muestra recuperación ≥ 2× la
  tarifa, el mes es gratis. Es la objeción-matadora convertida en promesa; el riesgo
  real es bajo porque el piloto filtra a los centros donde el servicio no rinde.
- **Promoción de partida:** piloto gratis 2 semanas + primer mes a mitad de precio si
  contrata el plan Completo al terminar el piloto.

### Canales (en orden)

1. **Puerta a puerta en terreno** (2–3 horas diarias, tiempo completo lo permite):
   consultas y centros alrededor de estaciones de metro y ejes comerciales de 2–3
   comunas. Es el canal principal los primeros 6 meses.
2. **Referidos entre profesionales de la salud:** al cerrar cada cliente, pedir 2
   contactos de colegas; ofrecer un mes con descuento por referido convertido.
3. **Gremios y comunidades:** asociaciones de dentistas/kinesiólogos, grupos de
   Facebook y WhatsApp de profesionales de la salud, congresos y ferias del rubro.
4. **WhatsApp/correo frío con el one-pager de resultados** (recién desde el mes 2,
   cuando existan datos reales de pilotos).

### Guion de venta puerta a puerta (literal)

Entrar en horario valle (10:30–12:00 o 15:30–17:00), preguntar por el dueño o
administrador. Con el one-pager impreso en la mano:

> "Hola, soy [nombre], de Confirma. Le robo 60 segundos. ¿Cuántos pacientes agendados
> no llegaron la semana pasada? [pausa — dejar que responda; casi todos saben que son
> varios]. Eso en Chile es entre el 15 y el 25 por ciento de las horas, y cada una es
> plata que no se factura. Nosotros confirmamos cada cita por WhatsApp dos veces,
> gestionamos las respuestas, y cuando alguien cancela, **llenamos ese cupo con su
> lista de espera el mismo día**. Usted no instala nada ni cambia su forma de
> agendar: nosotros operamos todo. Y se lo pruebo gratis: dos semanas de piloto con
> medición. Al final le muestro en una página cuántas horas recuperamos y cuánta
> plata era. Si el número no le hace sentido, quedamos como amigos. ¿Le parece que lo
> partamos con la agenda de la próxima semana?"

Objeciones frecuentes y respuestas:

- *"Mi secretaria ya llama."* → "Perfecto, no la reemplazamos: ella no alcanza a
  llamar a todos ni a rellenar cupos, y eso es justo lo que hacemos nosotros. Ella
  queda libre para atender el mesón. El piloto le muestra si aportamos algo sobre lo
  que ella ya logra: se mide, no se discute."
- *"Mi software de agenda ya manda recordatorios."* → "Bien, ese recordatorio ayuda.
  ¿Y quién lee las respuestas, reagenda y llena el cupo cuando alguien avisa que no
  va? Ese tramo es el que factura, y es el que hacemos nosotros."
- *"¿Y los datos de mis pacientes?"* → "Solo usamos nombre, teléfono y fecha de la
  cita. Nunca diagnósticos ni tratamientos. Firmamos un acuerdo de confidencialidad,
  y al terminar el contrato los datos se eliminan. Se lo dejo por escrito."
- *"No tengo presupuesto."* → "Por eso el piloto es gratis y después hay garantía: si
  un mes no le recupero al menos el doble de la tarifa, ese mes no paga. El servicio
  se paga con plata que hoy usted está perdiendo."

### Diseño del piloto gratis de 2 semanas (el corazón comercial)

**Objetivo:** producir un dato irrefutable y convertirlo en contrato.

1. **Línea base (día 0):** pedir al centro la agenda de las últimas 4 semanas: citas
   agendadas vs. asistidas → % de inasistencia base y facturación promedio por
   atención (si no la dan, usar rango estimado del rubro y decirlo).
2. **Operación (días 1–14):** registrar por cada cita: confirmación enviada,
   respuesta, asistió / no asistió / canceló, cupo liberado, cupo rellenado desde
   lista de espera. Todo en la planilla estándar (Airtable/Sheets).
3. **Qué medir:** % inasistencia con Confirma vs. base; nº de cupos liberados con
   aviso; nº de cupos rellenados; **facturación recuperada estimada** = (atenciones
   salvadas por reagendamiento + cupos rellenados) × ticket promedio del centro.
4. **Presentación (día 15, en persona, 1 página impresa):**
   > "Antes: 22% de inasistencia. Con Confirma: 9%. Horas recuperadas en 2 semanas:
   > 7. Facturación recuperada estimada: $280.000. Proyección mensual: ~$560.000.
   > Plan Completo: $110.000/mes, con garantía de 2×. ¿Partimos el 1° del mes?"
5. **Criterio interno:** si el piloto no muestra recuperación proyectada ≥ 2× la
   tarifa, no ofrecer contrato con garantía — ofrecer plan Básico o retirarse. No
   firmar clientes donde el número no da: la garantía es sagrada.
6. **Regla de cartera:** máximo 2 pilotos gratis simultáneos, para no regalar
   operación.

### Primeros 10 clientes (primeras 2–3 semanas)

Semana 1: montar el stack y el guion (días 1–2); mapear 60 consultas en 2 comunas con
planilla de prospección (día 2); visitar 15 consultas por día (días 3–5) → meta: 2
pilotos firmados. Semana 2: operar los 2 pilotos + seguir visitando (10/día) → meta: 2
pilotos más en fila. Semanas 3–4: presentar resultados, convertir 2–3 contratos,
pedir 2 referidos por cierre. Con tasa estimada de 1 piloto por cada 20 visitas y
conversión piloto→contrato de 60–70%, los primeros 10 clientes pagados llegan entre
los meses 2 y 3 (supuestos a validar en terreno desde la semana 1).

## 3. Cómo administrarla (plan operativo y financiero)

### Stack no-code concreto (costos mensuales estimados, en régimen)

| Herramienta | Para qué | Costo mensual estimado |
|---|---|---|
| Plataforma WhatsApp Business API (respond.io, Wati, Callbell o similar) | Envíos masivos, bandeja de respuestas, plantillas aprobadas | $50.000–$80.000 |
| Costo por conversación de Meta | ~$30–$60 por conversación iniciada (estimado); ~250 citas × 2 toques ≈ $15.000–$25.000 **por cliente** | variable |
| Make (o Zapier) | Automatizar: planilla → envío → registro de respuesta | $15.000 |
| Google Sheets (gratis) → Airtable al escalar | Agenda espejo, lista de espera, métricas por cliente | $0 → $20.000 |
| IA (Claude / ChatGPT plan pagado) | Redactar plantillas, clasificar respuestas, armar reportes | $20.000 |
| Dominio + correo profesional | Seriedad comercial | $3.000 |
| **Total fijo del stack** | | **~$90.000–$140.000/mes** |

Nota honesta: al inicio la "integración" con la agenda de cada centro es **humana**:
el centro comparte su agenda del día siguiente (foto, export o acceso de lectura) y
tú/el sistema la vuelcan a la planilla. No prometas integraciones técnicas que no
puedes construir; véndelo como virtud ("no toco su sistema, no instalo nada").

### Operación diaria (rutina tipo, tiempo completo)

- **8:30–10:00** — Volcar agendas del día siguiente de cada cliente; disparar
  confirmaciones automáticas; revisar respuestas de la noche; gestionar
  reagendamientos que el flujo automático no resolvió.
- **10:30–13:00** — Venta en terreno (visitas puerta a puerta). Innegociable: sin
  visitas no hay cartera.
- **14:00–15:30** — Relleno de cupos: contactar lista de espera de cada cupo liberado
  (mensaje automatizado + llamada si no responde en 1 hora).
- **15:30–17:00** — Segunda ronda de terreno o reuniones de cierre/presentación de pilotos.
- **17:00–18:00** — Registro del día, métricas por cliente, preparar agendas de mañana.
- **Viernes:** revisión semanal de números. **Fin de mes:** reporte de valor a cada
  cliente (es el producto que renueva el contrato) y facturación.

### Cuidado con datos de pacientes (precauciones básicas, no es asesoría legal)

Los datos de salud son **datos sensibles** bajo la ley chilena de protección de datos
(régimen vigente y nueva ley ya aprobada que endurece exigencias y multas — verificar
plazos de entrada en vigencia con un abogado). Precauciones mínimas desde el día 1:

1. **Minimización:** manejar solo nombre, teléfono, fecha/hora y profesional. **Nunca**
   diagnósticos, tratamientos ni notas clínicas en tus planillas o mensajes.
2. **Mensajes neutros:** "Le recordamos su hora en [nombre del centro] el jueves a
   las 16:00". No mencionar especialidad cuando sea sensible (salud mental, por ejemplo).
3. **Contrato con cada centro** con cláusula de confidencialidad y tratamiento de
   datos por encargo: plantilla redactada una vez por abogado (~$100.000–$150.000,
   una vez) y reutilizada.
4. **Consentimiento del paciente:** el centro informa que las confirmaciones llegan
   por WhatsApp; toda persona puede pedir no ser contactada y se respeta de inmediato
   (lista de exclusión en la planilla).
5. **Higiene de accesos:** cuentas con clave única y verificación en dos pasos;
   planillas nunca públicas; datos del cliente se eliminan al terminar el contrato y
   se deja constancia por escrito.

### Recursos para partir (estimación, dentro del presupuesto)

| Ítem | Costo estimado |
|---|---|
| Formalización (SpA por "Tu empresa en un día" + notaría + inicio de actividades SII, para poder facturar) | $150.000 |
| Plantilla de contrato + confidencialidad (abogado, una vez) | $120.000 |
| Stack tecnológico, 3 meses de colchón | $300.000 |
| Material de venta (one-pagers impresos, tarjetas, carpeta) | $50.000 |
| Transporte para venta en terreno (3 meses) | $90.000 |
| Reserva de emergencia operativa | $200.000 |
| **Total para partir** | **~$910.000** (cabe holgado en el rango $500.000–$2.000.000) |

### Costos, margen y punto de equilibrio (estimaciones)

- **Ticket promedio por cliente:** $85.000/mes (mezcla de planes Básico y Completo).
- **Costo variable por cliente:** ~$20.000/mes (conversaciones API y proporcional de
  plataforma por volumen). **Margen bruto por cliente: ~$65.000/mes.**
- **Costos fijos mensuales:** stack base $100.000 + transporte $30.000 + varios
  $30.000 ≈ **$160.000/mes** (sin sueldo del dueño).
- **Punto de equilibrio operativo:** $160.000 ÷ $65.000 ≈ **3 clientes**.
- **Para un sueldo de $800.000:** ($160.000 + $800.000) ÷ $65.000 ≈ **15 clientes**.
- Escenario mes 12 (estimación con supuestos comerciales cumplidos): 25–30 clientes →
  ingresos $2.100.000–$2.550.000/mes, margen tras costos ~$1.500.000–$1.900.000 antes
  de sueldo. El límite operativo de una persona se estima en 25–35 clientes; después
  se contrata.

### Indicadores semanales (mirar cada viernes)

1. Visitas de venta realizadas (meta: 40/semana los primeros meses).
2. Pilotos activos y propuestas presentadas.
3. Clientes activos y MRR (ingreso mensual recurrente).
4. % de inasistencia promedio de la cartera (la promesa central: debe bajar y
   mantenerse bajo la base de cada cliente).
5. Cupos rellenados desde lista de espera en la semana (la métrica que renueva contratos).
6. Bajas de clientes (churn) y su motivo.

### Riesgos y mitigación

| Riesgo | Mitigación |
|---|---|
| 1. Los software de agenda incorporan relleno de lista de espera y gestión de respuestas | Foco en centros chicos sin software o con software subutilizado; vender servicio administrado con responsable humano y garantía de resultado, que un software no ofrece; construir relación y reporte mensual que haga carero cambiarse. |
| 2. Dependencia de WhatsApp / alzas de precio de Meta (riesgo de plataforma, declarado desde el diseño) | Servicio canal-agnóstico (SMS/llamada como respaldo), contrato promete resultado y no canal; traspaso de costos por volumen ya incorporado en el precio. |
| 3. Incidente de privacidad con datos de pacientes | Protocolo de minimización y accesos desde el día 1, contrato con confidencialidad, eliminación de datos al término; ante cualquier incidente, aviso inmediato al centro. |
| 4. Churn por valor no percibido (el servicio funciona pero se vuelve invisible) | El reporte mensual de facturación recuperada es obligatorio y se presenta, no se manda; sin reporte no hay renovación. |

### Camino de crecimiento

- **Meses 1–3:** 2 comunas, venta en terreno diaria, 6–10 clientes. Señal de avance:
  conversión piloto→contrato ≥ 50%.
- **Meses 4–12:** 20–30 clientes, canal de referidos activo, sube la mezcla del plan
  Completo. Señal para contratar el primer gestor de cuentas part-time: 20 clientes o
  la operación diaria supera las 4 horas.
- **Año 2:** segunda vertical de hora agendada esencial (veterinarias, centros de
  atención kinésica domiciliaria, exámenes de laboratorio) y/o centros medianos con
  tarifas mayores. Eventual productización parcial (portal de reportes), siempre
  detrás del servicio, no delante.
- **Qué NO hacer aunque vaya bien:** no regalar más de 2 pilotos a la vez, no
  prometer integraciones técnicas, no crecer en clientes sin capacidad de operar el
  relleno (es la promesa que sostiene el precio).

## 4. Veredicto

- **Necesidad real: 8/10.** El cliente directo es el centro de salud, pero la
  necesidad servida es acceso a atención de salud: cada cupo rellenado es un paciente
  atendido antes. El dolor económico del centro es concreto, medible y mensual.
- **Prevalencia: 8/10.** La salud presencial y las agendas llenas de gente que a
  veces no llega existirán en 20 años. El único componente perecible es el canal
  (WhatsApp), y está aislado por diseño.
- **Facilidad de ejecución: 8/10.** Stack 100% no-code al alcance del perfil del
  dueño, inversión bajo $1.000.000, punto de equilibrio en ~3 clientes. La exigencia
  real es disciplina comercial: 40 visitas por semana durante meses.

**Recomendación: hacerla ya, con la validación integrada al arranque.** Los 2
primeros pilotos gratis SON la validación: costo casi cero, 30 días de plazo, y un
criterio limpio — si los pilotos no muestran recuperación ≥ 2× la tarifa o ningún
centro acepta piloto tras 60 visitas, revisar segmento (otra especialidad u otra
comuna) antes de insistir o descartar.
