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

> **Atajo (Windows)**: el script
> [`scripts/configure-shopify.ps1`](../scripts/configure-shopify.ps1) hace por
> API los pasos 2 y 3 de abajo (webhook + productos con SKUs correctos) desde
> tu PC, pidiendo el dominio y las credenciales de forma interactiva — no salen
> de tu máquina. El paso 1 (crear la app) y el 4 (COD) siguen siendo manuales.
> Es idempotente: puedes re-ejecutarlo sin duplicar nada.

> ⚠️ **No existe un token `shpat_` permanente para apps nuevas.** Desde el
> 1-ene-2026 no se pueden crear apps personalizadas en el admin, y las del Dev
> Dashboard **no muestran ningún token en la UI**: entregan Client ID + Client
> Secret, que se canjean por un token de **24 h** (*client credentials grant*).
> El gateway hace ese canje y lo renueva solo. Ver
> [Get API access tokens for Dev Dashboard apps](https://shopify.dev/docs/apps/build/dev-dashboard/get-api-access-tokens).

## Configuración en Shopify (una vez)

1. **App en el Dev Dashboard** — `https://dev.shopify.com/dashboard/`, con la
   **misma cuenta/organización dueña de la tienda** (el *client credentials
   grant* falla si la app y la tienda están en organizaciones distintas):
   - **Apps → Create app → Start from Dev Dashboard**, nombrarla y **Create**.
   - Pestaña **Versions**: *App URL* `https://shopify.dev/apps/default-app-home`
     (no es embebida), *Webhooks API Version* la más nueva, y **Scopes**:
     `read_products`, `write_products` (los usa el script que crea el catálogo),
     `read_orders`, `write_orders`, `read_fulfillments`, `write_fulfillments`
     (los usa el conector en runtime). Luego **Release** — sin esto los scopes
     no se aplican.
   - Pestaña **Home → Install app** → seleccionar la tienda → **Install**.
   - Pestaña **Settings**: copiar **Client ID** y **Client secret**.
2. **Webhook**: crearlo por API con `scripts/configure-shopify.ps1` (o a mano
   en *Configuración → Notificaciones → Webhooks*):
   - Evento: **Order creation** · Formato: JSON
   - URL: `https://api.tudominio.cl/webhooks/shopify`
   - **Secreto de firma**: los webhooks creados **por API** se firman con el
     **Client Secret de la app**; los creados a mano en el admin, con el
     secreto que muestra esa pantalla al pie. `SHOPIFY_WEBHOOK_SECRET` debe
     ser el que corresponda a cómo se creó el webhook.
3. **SKUs**: cada variante en Shopify debe tener como SKU el mismo valor que
   `products.sku` en la base interna. Un pedido con SKUs sin mapear no se
   procesa (queda en el log del gateway para corregir y reprocesar).
4. **Contra entrega** (opcional): *Settings → Payments → Manual payment
   methods → Cash on Delivery (COD)*.

## Configuración del sistema

En `infra/.env.prod` (o el entorno del gateway):

```bash
SHOPIFY_STORE_DOMAIN=mitienda.myshopify.com
SHOPIFY_CLIENT_ID=...             # Dev Dashboard → app → Settings
SHOPIFY_CLIENT_SECRET=...         # ídem
SHOPIFY_WEBHOOK_SECRET=...        # = Client Secret si el webhook se creó por API
SHOPIFY_API_VERSION=2026-04       # opcional; vacío usa el default del código
```

Sin `SHOPIFY_WEBHOOK_SECRET` el conector queda desactivado (el endpoint rechaza
todo, porque no puede verificar la firma). Sin `SHOPIFY_CLIENT_ID`/
`SHOPIFY_CLIENT_SECRET` el conector procesa pedidos igualmente, pero la
cancelación por falta de stock y la sincronización de tracking pasan a ser
manuales (queda aviso en el log).

**Gestión del token** — el gateway (`ShopifyService`) canjea Client ID/Secret
en `POST /admin/oauth/access_token` (`grant_type=client_credentials`), cachea
el token en memoria y lo renueva 5 minutos antes de vencer. Renovaciones
simultáneas se colapsan en una sola. Nada se persiste: al reiniciar, el primer
pedido vuelve a acuñarlo.

`SHOPIFY_ADMIN_TOKEN` sigue soportado y **tiene prioridad** si se define, pero
solo sirve para apps personalizadas creadas en el admin antes del 1-ene-2026.
Para una app nueva debe quedar vacío.

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
