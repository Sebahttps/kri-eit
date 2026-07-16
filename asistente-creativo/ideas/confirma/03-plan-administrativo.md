# Plan operativo y administrativo

> Cómo hacer funcionar el negocio día a día y mantenerlo sano financieramente.

- **Idea:** Confirma (ver ficha 01)
- **Fecha:** 2026-07-16

## 1. Operación diaria

- **Tareas de cada día para que el negocio funcione:** volcar las agendas del día
  siguiente de cada cliente a la planilla (la "integración" inicial es humana: foto,
  export o acceso de lectura del centro); disparar confirmaciones automáticas (48 h y
  3 h antes); gestionar respuestas que el flujo automático no resuelve; contactar
  lista de espera por cada cupo liberado (mensaje automatizado + llamada si no
  responde en 1 hora); registrar métricas por cliente; y venta en terreno todos los
  días hábiles.
- **Horario / rutina tipo:** 8:30–10:00 agendas y confirmaciones; 10:30–13:00 venta
  puerta a puerta; 14:00–15:30 relleno de cupos; 15:30–17:00 segunda ronda de terreno
  o cierres de piloto; 17:00–18:00 registro y preparación del día siguiente. Viernes:
  revisión de números. Fin de mes: reporte de valor presentado a cada cliente + facturación.
- **¿Quién hace qué?** Al inicio, el dueño hace todo con tres sombreros: *operador*
  (confirmaciones y relleno), *vendedor* (visitas y cierres) y *administrador*
  (números, facturas, reportes). Primer contratado (gestor de cuentas part-time)
  asume el sombrero de operador al llegar a ~20 clientes.

## 2. Recursos necesarios

| Recurso | Detalle | Costo estimado |
|---|---|---|
| Inversión inicial | Colchón del stack por 3 meses ($300.000) + reserva de emergencia operativa ($200.000) | $500.000 |
| Equipamiento | Computador y smartphone propios (supuesto declarado: ya los tiene) | $0 |
| Insumos / inventario inicial | One-pagers impresos, tarjetas, carpeta de venta | $50.000 |
| Local / espacio | Se trabaja desde casa y en terreno | $0 |
| Permisos / formalización | SpA por "Tu empresa en un día" + notaría + inicio de actividades SII (los centros exigen factura) + plantilla de contrato y confidencialidad hecha por abogado (una vez) | $270.000 |
| Personas | Solo el dueño hasta ~20 clientes | $0 |
| Transporte | Venta en terreno, 3 meses | $90.000 |
| **Total para partir** | | **~$910.000** (dentro del rango $500.000–$2.000.000) |

Stack no-code mensual en régimen (detalle en `00-propuesta.md`): plataforma WhatsApp
Business API $50.000–$80.000 + Make $15.000 + Sheets gratis (Airtable $20.000 al
escalar) + IA $20.000 + dominio/correo $3.000 ≈ **$90.000–$140.000/mes**, más
conversaciones de Meta ~$15.000–$25.000 por cliente (variable).

## 3. Costos y margen mensual (escenario mes 6: 15 clientes, estimación)

| Concepto | Monto mensual |
|---|---|
| Costos fijos (stack base $100.000 + transporte $30.000 + varios $30.000) | $160.000 |
| Costos variables (~$20.000 × 15 clientes) | $300.000 |
| **Total costos** | **$460.000** |
| Ventas esperadas (15 × ticket promedio $85.000) | $1.275.000 |
| **Margen (ventas − costos)** | **$815.000** (antes de sueldo del dueño e impuestos) |

## 4. Punto de equilibrio

- **¿Cuántos servicios hay que vender al mes para no perder dinero?** ~3 clientes
  activos cubren los costos del negocio; ~15 clientes cubren además un sueldo de
  dueño de $800.000.
- **Cálculo:** costos fijos $160.000 ÷ margen unitario $65.000 ($85.000 − $20.000
  variable) ≈ 2,5 → **3 clientes**. Con sueldo: ($160.000 + $800.000) ÷ $65.000 ≈
  14,8 → **15 clientes**.

## 5. Indicadores de la semana

| Indicador | Meta | ¿Cómo se mide? |
|---|---|---|
| Visitas de venta realizadas | 40/semana (primeros meses) | Planilla de prospección, cada visita anotada el mismo día |
| Pilotos activos + propuestas presentadas | 2 pilotos / ≥1 presentación semanal | Registro de pipeline |
| Clientes activos y MRR | Según meta del mes (mes 3: 8–10 y ~$700.000+) | Planilla de contratos y facturación |
| % inasistencia promedio de la cartera | ≤ 50% de la línea base de cada cliente | Planilla operativa: citas vs. asistencias por cliente |
| Cupos rellenados desde lista de espera | Creciente; es la métrica que renueva contratos | Registro de relleno por cupo liberado |
| Bajas de clientes (churn) y motivo | < 5% mensual | Registro de bajas con causa |

## 6. Riesgos principales

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| 1. Software de agenda incorpora relleno de cupos y gestión de respuestas | Media | Alto | Foco en centros chicos sin software o con software subutilizado; servicio administrado con responsable humano, garantía de resultado y reporte mensual presencial que un software no da |
| 2. Dependencia de WhatsApp / alzas de precio de Meta (riesgo de plataforma, declarado) | Media | Medio | Servicio canal-agnóstico (SMS/llamada de respaldo); contrato promete horas recuperadas, no mensajes; excedente por volumen ya traspasado al precio |
| 3. Incidente de privacidad con datos de pacientes | Baja | Alto | Minimización (solo nombre, teléfono, fecha/hora, profesional; nunca diagnósticos), mensajes neutros, contrato con confidencialidad, 2FA y planillas privadas, eliminación de datos al término, lista de exclusión para quien pida no ser contactado; aviso inmediato al centro ante cualquier incidente |
| 4. Churn por valor invisible (funciona tan bien que se olvida el dolor) | Media | Medio | Reporte mensual de facturación recuperada presentado en persona, obligatorio; garantía 2× mantiene el precio anclado al resultado |

## 7. Caja y disciplina financiera

- **Separación de dineros:** cuenta de la SpA separada del bolsillo personal desde la
  primera factura.
- **Sueldo del dueño:** $0 hasta el punto de equilibrio (mes 1–2 estimado); luego
  fijo mensual partiendo en $400.000 y subiendo con el MRR, nunca más del 60% del
  margen del mes.
- **Reserva de emergencia objetivo:** 3 meses de costos fijos (~$500.000) antes de
  cualquier gasto de expansión.
- **Día fijo de revisión de números:** todos los viernes a las 17:00; cierre mensual
  el último día hábil (facturación + reportes de valor a clientes).

## 8. Camino de crecimiento

- **Si funciona, ¿cómo escala?** Meses 1–3: 2 comunas, 6–10 clientes. Meses 4–12:
  20–30 clientes, canal de referidos activo, primer gestor de cuentas part-time al
  llegar a ~20 clientes u operación diaria sobre 4 horas. Año 2: nuevas verticales de
  hora agendada esencial (veterinarias, kinesiología domiciliaria, laboratorios),
  centros medianos con tarifas mayores, y productización parcial (portal de
  reportes) siempre detrás del servicio.
- **Señal que indica que es momento de escalar:** conversión piloto→contrato ≥ 50%
  sostenida por 2 meses, churn < 5% mensual y lista de espera de pilotos.
- **Qué NO hacer aunque vaya bien:** no regalar más de 2 pilotos simultáneos; no
  prometer integraciones técnicas que no se pueden construir; no sumar clientes sin
  capacidad real de operar el relleno de cupos (es la promesa que sostiene el
  precio); no endeudarse para crecer antes de tener la reserva de 3 meses.
