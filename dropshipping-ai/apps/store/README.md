# KRI·Tienda — Tienda B2C

Storefront Next.js 14 que consume el gateway (`business-api`) y el Agente
Front-Office (`agents-service`).

- **Catálogo** (`/`): productos activos vía `GET /products` del gateway, con
  badge de tendencia y las 5 promesas siempre visibles.
- **Carrito**: contexto React persistido en `localStorage`, drawer lateral.
- **Checkout** (`/checkout`): crea el pedido y ejecuta el flujo real —
  el Agente B2B confirma stock antes de habilitar cualquier cobro; contra
  entrega queda confirmado con OC emitida; online pasa por `pay`.
  Si el proveedor no confirma stock, no se cobra y se informa (promesa a).
- **Pedido** (`/pedido/[id]`): línea de progreso, hora exacta de la
  confirmación de stock, seguimiento en tiempo real (se refresca solo) y
  estado de garantía/retracto.
- **Chat**: widget flotante conectado a `POST /front-office/chat` — el Agente
  B2C vende, verifica stock y gestiona garantías/retractos en la conversación.

## Desarrollo

```bash
npm install
BUSINESS_API_URL=http://localhost:4000 AGENTS_API_URL=http://localhost:8000 npm run dev
# http://localhost:3001
```

Los rewrites de Next (`/api/gw/*`, `/api/agents/*`) evitan CORS y ocultan las
URLs internas.
