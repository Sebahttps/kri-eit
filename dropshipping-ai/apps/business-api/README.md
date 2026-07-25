# Business API — Gateway de negocio (Paso 4)

NestJS (TypeScript). Se construye en el Paso 4:

- Auth de supervisores (tabla `supervisors`).
- Pedidos y pagos (respetando el trigger `trg_pago_requiere_stock`).
- WebSocket gateway: push de KPIs y nuevas Sugerencias IA al dashboard.
- Webhooks de carriers → `shipment_events` (seguimiento en tiempo real).
