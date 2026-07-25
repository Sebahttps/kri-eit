# Business API — Gateway de negocio

NestJS (TypeScript). La capa de negocio entre la tienda, el dashboard y los agentes.

## Módulos

- **auth**: login de supervisores (`POST /auth/login`, bcrypt + JWT 8 h).
  `JwtAuthGuard` protege los endpoints de administración.
- **orders**: ciclo de vida del pedido respetando las promesas:
  - `POST /orders` — crea el pedido en `carrito` (cliente + ítems, total calculado).
  - `POST /orders/:id/checkout` — el Agente B2B confirma stock (promesa a);
    `contra_entrega` queda confirmado y emite OC al tiro (promesa b);
    `online` pasa a `pago_pendiente`.
  - `POST /orders/:id/pay` — punto de integración del PSP (Webpay/MercadoPago);
    marca pagado y emite la OC (el trigger de la base re-valida el stock).
  - `GET /orders/:id` — detalle con envío; `GET /orders` — listado (JWT).
- **webhooks**: `POST /webhooks/carrier` — eventos del courier alimentan
  `shipment_events` (promesa c); `entregado` dispara en la base la garantía de
  6 meses y la ventana de retracto (promesas d y e).
- **realtime**: WebSocket (socket.io, namespace `/eventos`):
  - Postgres `LISTEN eventos` (migración `001_notify_events.sql`) → evento
    `evento` con cada sugerencia, cambio de pedido, seguimiento o ticket.
  - Snapshot de KPIs cada 10 s → evento `kpis`.

## Desarrollo

```bash
npm install && npm run build
BUSINESS_DATABASE_URL=postgresql://... AGENTS_API_URL=http://localhost:8000 npm start
# API en http://localhost:4000 · WS en ws://localhost:4000/eventos
```

Variables: `BUSINESS_DATABASE_URL`, `AGENTS_API_URL`, `BUSINESS_JWT_SECRET`
(obligatoria en producción), `BUSINESS_CORS_ORIGIN`, `PORT`.

El seed crea el supervisor `sebastianmenat@gmail.com`; la contraseña no está en
el repo (solo su hash bcrypt en `db/seed.sql`). Para usar la tuya en desarrollo,
genera un hash y reemplázalo (ver `docs/deploy-production.md`, sección
"Cambiar la contraseña del Supervisor").
