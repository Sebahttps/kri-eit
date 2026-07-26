# Modo híbrido con Shopify

Shopify actúa como vitrina y checkout; los agentes siguen siendo el back-office
real: cada pedido de Shopify entra por webhook, se registra como pedido interno
y recorre el flujo existente — el Agente B2B verifica stock con el proveedor,
emite la OC, y sobre el umbral de autonomía escala al Supervisor. El dashboard,
los KPIs, la auditoría y los webhooks de carriers funcionan igual.

## Qué cambia respecto de la tienda propia

| Promesa | Tienda propia | Híbrido con Shopify |
|---|---|---|
| (a) Stock antes de pagar | El pago **no existe** sin stock confirmado (trigger) | Shopify cobra primero; sin stock ⇒ **cancelación y reembolso inmediatos** |
| (b) Contra entrega | Nativa | Método de pago manual "Cash on Delivery" de Shopify |
| (c) Seguimiento | WebSocket propio | El tracking se **sincroniza al pedido de Shopify** (fulfillment + email) |
| (d) y (e) Garantía y retracto | Triggers automáticos | **Sin cambios** (viven en la base interna) |

La tienda propia (`apps/store`) puede seguir corriendo como canal secundario:
ambos canales convergen en el mismo flujo de pedidos.

## Configuración en Shopify (una vez)

1. **App personalizada**: Admin de Shopify → *Settings → Apps and sales
   channels → Develop apps → Create an app*. Scopes de Admin API:
   `read_orders`, `write_orders`, `read_fulfillments`, `write_fulfillments`.
   Instalar la app y copiar el **Admin API access token** (`shpat_...`).
2. **Webhook**: *Settings → Notifications → Webhooks → Create webhook*:
   - Evento: **Order creation** · Formato: JSON
   - URL: `https://api.tudominio.cl/webhooks/shopify`
   - Copiar el **secreto de firma** que muestra Shopify al pie de la lista.
3. **SKUs**: cada variante en Shopify debe tener como SKU el mismo valor que
   `products.sku` en la base interna. Un pedido con SKUs sin mapear no se
   procesa (queda en el log del gateway para corregir y reprocesar).
4. **Contra entrega** (opcional): *Settings → Payments → Manual payment
   methods → Cash on Delivery (COD)*.

## Configuración del sistema

En `infra/.env.prod` (o el entorno del gateway):

```bash
SHOPIFY_WEBHOOK_SECRET=...        # secreto de firma del webhook
SHOPIFY_STORE_DOMAIN=mitienda.myshopify.com
SHOPIFY_ADMIN_TOKEN=shpat_...
```

Con las tres vacías el conector queda desactivado (el endpoint rechaza todo).
Sin `SHOPIFY_ADMIN_TOKEN` el conector procesa pedidos igualmente, pero la
cancelación por falta de stock y la sincronización de tracking pasan a ser
manuales (queda aviso en el log).

## Flujo resultante

```
Pedido en Shopify ──webhook──▶ gateway (verifica firma HMAC, dedup)
  ├─ pago capturado por Shopify ─▶ Agente B2B verifica stock
  │     ├─ stock OK  ─▶ pedido 'pagado' + OC (o Sugerencia IA sobre el umbral)
  │     └─ sin stock ─▶ cancelación + reembolso en Shopify (promesa a, degradada)
  └─ COD ─▶ igual, como 'contra_entrega_confirmado' (promesa b)

Carrier ──webhook──▶ seguimiento interno (promesa c)
  └─ primer 'despachado' ─▶ fulfillment + tracking en Shopify (email al cliente)
Entregado ─▶ garantía 6 meses + ventana retracto 10 días (promesas d y e, triggers)
```

## Prueba de punta a punta

1. Crear un pedido de prueba en Shopify (o *Send test notification* del
   webhook, que valida firma y respuesta).
2. Verificar en el dashboard que el pedido aparece y que la OC se emitió (o
   que hay una Sugerencia IA esperando aprobación si superó el umbral).
3. Simular el carrier: `POST /webhooks/carrier` con `despachado` → el pedido
   de Shopify queda *fulfilled* con tracking y el cliente recibe el email.
